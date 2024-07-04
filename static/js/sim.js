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
