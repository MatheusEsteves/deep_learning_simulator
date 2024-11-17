import asyncio
import websockets
import nbformat
from jupyter_client import KernelManager
from notebook import notebookapp
from notebook.services.contents.filemanager import FileContentsManager
from IPython import get_ipython

# Função para executar o notebook
def execute_notebook(notebook_path):
    """
    Executa um notebook Jupyter e retorna a saída da execução
    """
    # Abrir o notebook
    with open(notebook_path) as f:
        notebook_content = nbformat.read(f, as_version=4)
    
    # Criar o KernelManager
    km = KernelManager()
    km.start_kernel()
    kernel = km.client()
    kernel.start_channels()

    # Executar as células do notebook
    exec_result = []
    for cell in notebook_content.cells:
        if cell.cell_type == 'code':
            # Executar a célula de código
            kernel.execute(cell.source)
            # Obter a resposta da execução da célula
            message = kernel.get_iopub_msg(timeout=60)
            exec_result.append(message)

    # Parar o kernel após a execução
    kernel.stop_channels()
    km.shutdown_kernel()

    return exec_result

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

        NOTEBOOK_PATH = "bertviz_model.ipynb"
        try:
            result = execute_notebook(NOTEBOOK_PATH)
            print(f"Result : {result}")
        except Exception as e:
            print(f"Erro ao rodar modelo no BertViz: {str(e)}")
        
        await asyncio.Future()  # Manter o servidor rodando

# Iniciar o servidor WebSocket
if __name__ == "__main__":
    asyncio.run(main())