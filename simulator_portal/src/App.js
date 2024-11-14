import React, { useState } from 'react';
import useWebSocket from 'react-use-websocket';

function App() {
  const [message, setMessage] = useState("");
  const [receivedMessage, setReceivedMessage] = useState("");
  
  // URL do servidor WebSocket
  const socketUrl = "ws://localhost:8765";
  
  // Usando o hook useWebSocket
  const { sendMessage, lastMessage } = useWebSocket(socketUrl, {
    onOpen: () => console.log("Conectado ao servidor WebSocket"),
    onMessage: (event) => setReceivedMessage(event.data),
  });

  // Função para enviar mensagem para o servidor WebSocket
  const handleSendMessage = () => {
    if (message) {
      sendMessage(message);
      setMessage(""); // Limpa o campo de mensagem após o envio
    }
  };

  return (
    <div className="App">
      <h1>WebSocket com React e Python</h1>
      
      <div>
        <input 
          type="text" 
          value={message} 
          onChange={(e) => setMessage(e.target.value)} 
          placeholder="Digite uma mensagem"
        />
        <button onClick={handleSendMessage}>Enviar</button>
      </div>
      
      <div>
        <h2>Mensagem Recebida:</h2>
        <p>{receivedMessage}</p>
      </div>
    </div>
  );
}

export default App;
