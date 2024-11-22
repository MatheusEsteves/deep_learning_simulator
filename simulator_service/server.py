import asyncio
import websockets
import time
from jupyter_client import KernelManager
import os
import json

def remove_notebook_cell_previous_execution_output():
    if os.path.exists('outputs/cell_execution_output.html'):
        os.remove('outputs/cell_execution_output.html')

def save_notebook_cell_execution_output(content_data):
    with open('outputs/cell_execution_output.html', 'a') as output_file:
        if 'text/html' in content_data:
            output_file.write(content_data['text/html'])

        if 'application/javascript' in content_data:
            output_file.write(f"<script>{content_data['application/javascript']}</script>")

        output_file.close()

# Função para executar uma célula de código no Jupyter
def run_code_cell(code, arguments, imports):
    # Criação de um KernelManager para gerenciar o kernel
    km = KernelManager()
    
    try:
        print("Inicializando kernel para comunicação com jupyter notebook")
        km.start_kernel()  # Inicia o kernel
    except Exception as e:
        print(f"Erro ao inicializar kernel para conexão com o jupyter notebook: {str(e)}")

    kernel = km.client()  # Obtém o cliente para o kernel

    try:
        print("Inicializando canais de comunicação do jupyter client")
        kernel.start_channels()  # Abre os canais de comunicação
    except Exception as e:
        print(f"Erro ao abrir canais de comunicação do jupyter client: {str(e)}")

    # Imports necessários de libs antes de inicializar as próximas células
    try:
        print("Inicializando passagem de parâmetros e atribuição de valores")
        for import_lib in imports:
            kernel.execute(import_lib)
    except Exception as e:
        print(f"Erro ao rodar célula no notebook: {str(e)}")

    # Passagem de parâmetros para declaração e atribuição de valores
    try:
        print("Inicializando passagem de parâmetros e atribuição de valores")
        for argument_key in list(arguments.keys()):
            kernel.execute(f"{argument_key} = {arguments[argument_key]}")
    except Exception as e:
        print(f"Erro ao rodar célula no notebook: {str(e)}")

    # Executa o código
    try:
        print("Inicializando execução do código da célula no jupyter notebook")
        kernel.execute(code)
    except Exception as e:
        print(f"Erro ao rodar célula no notebook: {str(e)}")

    remove_notebook_cell_previous_execution_output()

    # Aguardar até que a execução seja concluída
    while True:
        # Obtém a resposta do kernel (status da execução)
        msg = ''
        try:
            msg = kernel.get_iopub_msg(timeout=10)  # Espera por mensagens do kernel (ex: execução)
        except Exception as e:
            break

        if msg and 'header' in msg:
            print("Mensagem recebida na execução da célula [HEADER] : ", msg['header'])
            if msg['header']['msg_type'] == 'display_data':
                print("Formatos retornados pela execução da célula : ", list(msg['content']['data'].keys()))
                save_notebook_cell_execution_output(msg['content']['data'])
            elif msg['header']['msg_type'] == 'status' and msg['content']['execution_state'] == 'idle':
                print("Execução da célula finalizada com sucesso")
            elif msg['header']['msg_type'] == 'error':
                print(f"Execução da célula com erro : {msg['content']}")
        else:
            # Se não houver mensagem, continue esperando
            try:
                time.sleep(0.1)
            except Exception as e:
                print(f"Erro ao tentar rodar time.sleep: {e}")

    # Parar os canais e o kernel após a execução
    try:
        kernel.stop_channels()
        km.shutdown_kernel()
    except Exception as e:
        print(f"Erro ao tentar parar os canais de comunicação e o kernel após execução da celula: {str(e)}")

def run_transformer_with_attention(payload):
    with open('notebook_cells_code/bertviz_model.py', 'r') as bertviz_model_code_file:
        try:
            arguments = {
                'sentence_a': f"'{payload['sentence_a']}'",
                'sentence_b': f"'{payload['sentence_b']}'",
                'visualization_mode': f"'{payload['visualization_mode']}'"
            }
            imports = ['!pip install bertviz']
            run_code_cell(bertviz_model_code_file.read(), arguments, imports)

            output_html_file_str = ''

            with open('outputs/cell_execution_output.html', 'r') as output_html_file:
                output_html_file_str = output_html_file.read()
            
            return {
                'event_response_type': 'run_transformer_with_attention',
                'event_response_payload': output_html_file_str 
            }
        except Exception as e:
            print(f"Erro ao rodar modelo no BertViz: {str(e)}")

# Função que gerencia as conexões WebSocket
async def echo(websocket):
    print(f"Nova conexão: {websocket.remote_address}")

    event_actions = {
        'run_transformer_with_attention': run_transformer_with_attention
    }
    
    try:
        # Continuar recebendo mensagens do cliente
        async for message in websocket:
            print(f"Mensagem recebida: {message}")
            try:
                message_dict = json.loads(message)
                response = event_actions[message_dict['event_action_type']](message_dict['event_payload'])
                await websocket.send(json.dumps(response))
            except Exception as e:
                print(f"Erro ao tentar ler mensagem enviada pelo client : {str(e)}")
    except websockets.exceptions.ConnectionClosed:
        print(f"Conexão fechada: {websocket.remote_address}")
        

# Configuração do servidor WebSocket
async def main():
    async with websockets.serve(echo, "localhost", 8765):
        print("Servidor WebSocket iniciado em ws://localhost:8765")
        
        await asyncio.Future()  # Manter o servidor rodando

# Iniciar o servidor WebSocket
if __name__ == "__main__":
    asyncio.run(main())