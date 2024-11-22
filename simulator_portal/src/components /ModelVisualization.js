import React from "react";
import "./ModelVisualization.css";

function ModelVisualization({ html }) {
    return (
        <div class="model-visualization-area">
            <iframe srcDoc={html} sandbox="allow-scripts" width="100%" height="1000vh" />
            <div class="model-visualization-metrics">
                <div className="model-visualization-metrics-label">
                    MÉTRICAS DE AVALIAÇÃO (TO DO)
                </div>
            </div>
        </div>
    )
}

export default ModelVisualization;