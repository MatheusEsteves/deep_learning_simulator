import React, { useState } from "react";
import useWebSocket from 'react-use-websocket';
import ModelVisualization from "./ModelVisualization";
import { ClipLoader } from 'react-spinners';
import "./Home.css";

function Home() {
    const [sentenceA, setSentenceA] = useState("");
    const [sentenceB, setSentenceB] = useState("");
    const [viewMode, setViewMode] = useState("");
    const [receivedMessage, setReceivedMessage] = useState({});
    const [loading, setLoading] = useState(false);
    
    // URL do servidor WebSocket
    const socketUrl = "ws://localhost:8765";
    
    // Usando o hook useWebSocket
    const { sendMessage, _ } = useWebSocket(socketUrl, {
        onOpen: () => console.log("Conectado ao servidor WebSocket"),
        onMessage: (event) => {
            const response = JSON.parse(event.data);
            setLoading(false);
            setReceivedMessage(response)
        },
    });

    // Função para enviar mensagem para o servidor WebSocket
    const handleSendMessage = (viewMode) => {
        const message = {
            'event_action_type': 'run_transformer_with_attention',
            'event_payload': {
                'sentence_a': sentenceA,
                'sentence_b': sentenceB,
                'visualization_mode': viewMode
            }
        }
        setLoading(true);
        sendMessage(JSON.stringify(message));
    };

    const handleChangeSentenceA = (e) => {
        setSentenceA(e.target.value);
    }

    const handleChangeSentenceB = (e) => {
        setSentenceB(e.target.value);
    }

    const handleViewMode = (e) => {
        setViewMode(e.target.value);
        handleSendMessage(e.target.value);
    }

    return (
        <div className="App">
            <div class="model-form">
                <h1>Deep Learning Simulator</h1>

                <h2>Primeira Sentença</h2>
                <textarea
                    value={sentenceA}             
                    onChange={handleChangeSentenceA} 
                    rows="2"
                    cols="20"
                    placeholder="Digite a primeira sentença"
                />

                <h2>Segunda Sentença</h2>
                <textarea
                    value={sentenceB}             
                    onChange={handleChangeSentenceB} 
                    rows="2"
                    cols="20"
                    placeholder="Digite a segunda sentença"
                />

                <select value={viewMode} onChange={handleViewMode}>
                    <option value="">Selecione o modo de visualização</option>
                    <option value="head_view">Head View</option>
                    <option value="model_view">Model View</option>
                    <option value="neuron_view">Neuron View</option>
                </select>
            </div>

            <div class="model-result">
                {loading ? (
                    <ClipLoader size={200} color="#3498db" loading={loading} />
                ) : (
                    <ModelVisualization html={receivedMessage['event_response_payload']} />
                )}
            </div>
        </div>
    );
}

export default Home;