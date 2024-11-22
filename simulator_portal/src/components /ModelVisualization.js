import React, { useState } from "react";

function ModelVisualization({ html }) {
    return (
        <iframe srcDoc={html} sandbox="allow-scripts" width="100%" height="1000vh" />
    )
}

export default ModelVisualization;