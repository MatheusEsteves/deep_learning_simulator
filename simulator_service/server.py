import asyncio
import websockets

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
        await asyncio.Future()  # Manter o servidor rodando

# Iniciar o servidor WebSocket
if __name__ == "__main__":
    asyncio.run(main())