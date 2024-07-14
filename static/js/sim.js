// Javascript for the slider
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

    // Define agents with colors
    const agents = [
        { x: 50, y: 50, color: '#ff0000' }, 
        { x: 100, y: 100, color: '#00ff00' },
    
    ];

    let animationCount = 0;
    const totalAnimations = 3; 

    function drawAgents() {
        ctx.clearRect(0, 0, canvas.width, canvas.height); 
        agents.forEach(agent => {
            ctx.fillStyle = agent.color;
            ctx.beginPath();
            ctx.arc(agent.x, agent.y, 10, 0, Math.PI * 2);
            ctx.fill();
        });

        agents.forEach(agent => {
            agent.x += Math.random() * 2 - 1;
            agent.y += Math.random() * 2 - 1;
        });

        animationCount++;

        if (animationCount < totalAnimations) {
            requestAnimationFrame(drawAgents);
        }
    }

    drawAgents();
});

