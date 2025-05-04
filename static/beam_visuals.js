function drawDiagrams(type, deflection, beamLength) {
    // Replace beamCanvas with summary info
    const beamCanvas = document.getElementById('beamCanvas');
    beamCanvas.style.display = "none";

    const summaryDiv = document.createElement("div");
    summaryDiv.className = "output";
    summaryDiv.innerHTML = `
        <h3>Mechanical Summary</h3>
        <ul>
            <li><strong>Beam Length:</strong> ${beamLength.toFixed(2)} m</li>
            <li><strong>Load Type:</strong> ${type === "point" ? "Point Load at Center" : type === "uniform" ? "Uniformly Distributed Load" : "End Moment (Cantilever)"}</li>
            <li><strong>Max Deflection:</strong> ${(deflection).toExponential(3)} m</li>
            <li><strong>Max Deflection Location:</strong> ${type === "moment" ? "At free end" : "At center of beam"}</li>
            <li><strong>Reactions:</strong> ${type === "moment" ? "Fixed end reaction moment only" : "Symmetrical reactions at both supports"}</li>
        </ul>
        <p style="font-style: italic; color: #ccc;">Note: Diagrams assume linear elastic behavior. No buckling or yield considered.</p>
    `;
    beamCanvas.parentNode.insertBefore(summaryDiv, beamCanvas);

    const width = 800;
    const margin = 50;

    // MOMENT DIAGRAM
    const momentCanvas = document.getElementById('momentCanvas');
    const mctx = momentCanvas.getContext('2d');
    mctx.clearRect(0, 0, momentCanvas.width, momentCanvas.height);
    const my = momentCanvas.height / 2;

    mctx.beginPath();
    mctx.moveTo(margin, my);
    if (type === "point") {
        mctx.lineTo(width / 2, my - 50);
        mctx.lineTo(width - margin, my);
    } else if (type === "uniform") {
        mctx.quadraticCurveTo(width / 2, my - 60, width - margin, my);
    } else if (type === "moment") {
        mctx.lineTo(width - margin, my - 50);
    }
    mctx.lineWidth = 3;
    mctx.strokeStyle = "orange";
    mctx.stroke();

    mctx.fillStyle = "#fff";
    mctx.fillText("Moment Diagram", margin, 20);
    mctx.beginPath();
    mctx.moveTo(margin, my);
    mctx.lineTo(width - margin, my);
    mctx.setLineDash([5, 5]);
    mctx.strokeStyle = "#666";
    mctx.stroke();
    mctx.setLineDash([]);

    // SHEAR DIAGRAM
    const shearCanvas = document.getElementById('shearCanvas');
    const sctx = shearCanvas.getContext('2d');
    sctx.clearRect(0, 0, shearCanvas.width, shearCanvas.height);
    const sy = shearCanvas.height / 2;

    sctx.beginPath();
    sctx.moveTo(margin, sy);
    if (type === "point") {
        sctx.lineTo(width / 2, sy - 50);
        sctx.lineTo(width - margin, sy + 50);
    } else if (type === "uniform") {
        sctx.lineTo(width - margin, sy + 50);
    } else if (type === "moment") {
        sctx.lineTo(width - margin, sy - 50);
    }
    sctx.lineWidth = 3;
    sctx.strokeStyle = "lime";
    sctx.stroke();

    sctx.fillStyle = "#fff";
    sctx.fillText("Shear Force Diagram", margin, 20);
    sctx.beginPath();
    sctx.moveTo(margin, sy);
    sctx.lineTo(width - margin, sy);
    sctx.setLineDash([5, 5]);
    sctx.strokeStyle = "#666";
    sctx.stroke();
    sctx.setLineDash([]);
}
