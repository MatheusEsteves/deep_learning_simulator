import React, { useState } from "react";
import useWebSocket from 'react-use-websocket';
import ModelVisualization from "./ModelVisualization";
import { ClipLoader } from 'react-spinners';
import "./Home.css";

function Home() {
    const [textSentenceTrain, setTextSentenceTrain] = useState("");
    const [textSentenceTrainB, setTextSentenceTrainB] = useState("");
    const [viewMode, setViewMode] = useState("");
    const [embedSize, setEmbedSize] = useState(0);
    const [numHeads, setNumHeads] = useState(0);
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
                'text_sentence_train': textSentenceTrain,
                'text_sentence_train_b': textSentenceTrainB,
                'visualization_mode': viewMode,
                'embed_size': embedSize,
                'num_heads': numHeads
            }
        }
        setLoading(true);
        sendMessage(JSON.stringify(message));
    };

    const handleChangeTextSentenceTrain = (e) => {
        setTextSentenceTrain(e.target.value);
    }

    const handleChangeTextSentenceTrainB = (e) => {
        setTextSentenceTrainB(e.target.value);
    }

    const handleChangeViewMode = (e) => {
        setViewMode(e.target.value);
        handleSendMessage(e.target.value);
    }

    const handleChangeEmbedSize = (e) => {
        setEmbedSize(e.target.value);
    }

    const handleChangeNumHeads = (e) => {
        setNumHeads(e.target.value);
    }

    return (
        <div className="App">
            <div class="model-form">
                <h1>Deep Learning Simulator</h1>

                <h2>Sentença A</h2>
                <textarea
                    value={textSentenceTrain}             
                    onChange={handleChangeTextSentenceTrain} 
                    rows="2"
                    cols="20"
                    placeholder="Digite o primeiro texto com palavras para treinamento"
                />

                <h2>Sentença B</h2>
                <textarea
                    value={textSentenceTrainB}             
                    onChange={handleChangeTextSentenceTrainB}
                    rows="2"
                    cols="20"
                    placeholder="Digite o segundo texto com palavras para treinamento"
                />

                <h2>Número de dimensões para embedding</h2>
                <input type="number" value={embedSize} onChange={handleChangeEmbedSize} />

                <h3>Número de heads para atenção</h3>
                <input type="number" value={numHeads} onChange={handleChangeNumHeads} />

                <select value={viewMode} onChange={handleChangeViewMode}>
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