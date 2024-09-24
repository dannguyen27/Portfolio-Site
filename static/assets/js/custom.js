document.addEventListener('DOMContentLoaded', function() {
    const osakaImage = document.getElementById('portfolio-img-1');
    
    if (osakaImage) {
        osakaImage.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default link behavior
            console.log('Image clicked'); // Log to console

            // Get the relative click coordinates
            const rect = osakaImage.getBoundingClientRect();
            const x = (event.clientX - rect.left) / rect.width;
            const y = (event.clientY - rect.top) / rect.height;

            // Make an AJAX request to the Flask server to get the color
            fetch(`/get-color?image=Osaka.jpg&x=${x}&y=${y}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error(data.error);
                    } else {
                        // Update the color information
                        const colorInfo = document.getElementById('color-info');
                        const colorBox = document.getElementById('color-box');

                        const r = data.r;
                        const g = data.g;
                        const b = data.b;

                        // Display the RGB values
                        colorInfo.textContent = `R: ${r}, G: ${g}, B: ${b}`;

                        // Set the background color of the color box
                        colorBox.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    } else {
        console.error('Image element not found');
    }
});
