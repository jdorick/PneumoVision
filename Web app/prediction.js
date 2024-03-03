// Function to trigger prediction
function predictImage() {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];

    if (file) {
        // Create a FormData object to send the file to the server
        const formData = new FormData();
        formData.append('image', file);

        // Make a POST request to the backend endpoint
        fetch('http://localhost:5000/predict', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(result => {
            // Display the results
            displayPredictionResults(result);
        })
        .catch(error => console.error('Error:', error));
    }
}