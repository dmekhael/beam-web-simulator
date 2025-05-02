function drawBeam(loadType, deflectionAmount) {
    const canvas = document.getElementById('beamCanvas');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const width = canvas.width;
    const height = canvas.height;
    const beamY = height / 2;

    // Base line
    ctx.beginPath();
    ctx.moveTo(50, beamY);
    ctx.lineTo(width - 50, beamY);
    ctx.lineWidth = 10;
    ctx.strokeStyle = "#00f4ff";
    ctx.stroke();

    // Simulated deflection arc (simplified)
    if (deflectionAmount > 0) {
        ctx.beginPath();
        ctx.moveTo(50, beamY);
        ctx.quadraticCurveTo(width / 2, beamY + deflectionAmount, width - 50, beamY);
        ctx.lineWidth = 5;
        ctx.strokeStyle = "#ff00ff";
        ctx.stroke();
    }
}
