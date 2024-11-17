import asyncio
import websockets
import time
from jupyter_client import KernelManager

# Função para executar uma célula de código no Jupyter
def run_code_cell(code):
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

    # Executa o código
    try:
        print("Inicializando execução do código da célula no jupyter notebook")
        kernel.execute(code)
    except Exception as e:
        print(f"Erro ao rodar célula no notebook: {str(e)}")
    
    # Aguardar até que a execução seja concluída
    while True:
        # Obtém a resposta do kernel (status da execução)
        try:
            msg = kernel.get_iopub_msg(timeout=1)  # Espera por mensagens do kernel (ex: execução)
            if msg:
                # Verifica se a execução terminou
                if msg['header']['msg_type'] == 'execute_result' or msg['header']['msg_type'] == 'stream':
                    # Se a execução resultou em saída ou stream, pegamos a saída
                    print("Resultado da execução:", msg['content'])
                    break
            else:
                # Se não houver mensagem, continue esperando
                time.sleep(0.1)
        except Exception as e:
            print(f"Erro ao tentar obter resposta de execução da célula no jupyter notebook: {e}")

    # Parar os canais e o kernel após a execução
    try:
        kernel.stop_channels()
        km.shutdown_kernel()
    except Exception as e:
        print(f"Erro ao tentar parar os canais de comunicação e o kernel após execução da celula: {str(e)}")

# Função que gerencia as conexões WebSocket
async def echo(websocket):
    print(f"Nova conexão: {websocket.remote_address}")
    
    try:
        # Continuar recebendo mensagens do cliente
        async for message in websocket:
            print(f"Mensagem recebida: {message}")
            # Enviar a mesma mensagem de volta (eco)
            await websocket.send(f"Recebido: {message}")
    except websockets.exceptions.ConnectionClosed:
        print(f"Conexão fechada: {websocket.remote_address}")
        

# Configuração do servidor WebSocket
async def main():
    async with websockets.serve(echo, "localhost", 8765):
        print("Servidor WebSocket iniciado em ws://localhost:8765")

        with open('notebook_cells_code/bertviz_model.py', 'r') as bertiz_model_code_file:
            try:
                run_code_cell(bertiz_model_code_file.read())
            except Exception as e:
                print(f"Erro ao rodar modelo no BertViz: {str(e)}")
        
        await asyncio.Future()  # Manter o servidor rodando

# Iniciar o servidor WebSocket
if __name__ == "__main__":
    asyncio.run(main())