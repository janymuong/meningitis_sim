// JavaScript for the slider
document.addEventListener('DOMContentLoaded', function() {
    const sliders = document.querySelectorAll('.slider');
    
    sliders.forEach(slider => {
        const output = document.createElement('span');
        slider.parentNode.insertBefore(output, slider.nextSibling);
        output.innerHTML = slider.value;

        slider.oninput = function() {
            output.innerHTML = this.value;
        };
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('agentCanvas');
    const ctx = canvas.getContext('2d');

    // Set canvas dimensions
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Define agents with colors
    const agents = [
        { x: 150, y: 170, color: '#ff0000' }, // Red
        { x: 320, y: 320, color: '#00ff00' }, // Green
        { x: 970, y: 205, color: '#0000ff' }  // Blue
    ];

    function drawPhagocyte(ctx, x, y, color) {
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.moveTo(x + Math.random() * 30 - 15, y + Math.random() * 30 - 15);
        for (let i = 0; i < 10; i++) {
            ctx.lineTo(x + Math.random() * 100 - 50, y + Math.random() * 100 - 50);
        }
        ctx.closePath();
        ctx.fill();
    }

    function drawAgents() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        agents.forEach(agent => {
            drawPhagocyte(ctx, agent.x, agent.y, agent.color);
        });

        agents.forEach(agent => {
            agent.x += Math.random() * 4 - 2;
            agent.y += Math.random() * 4 - 2;
        });

        requestAnimationFrame(drawAgents);
    }

    drawAgents();
});
