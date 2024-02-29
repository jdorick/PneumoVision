// let uploadedFilePath; // Global variable to store the uploaded image path

// function handleUpload() {
//     displayLoadingBar();
//     const fileInput = document.getElementById('uploadInput');
//     const files = fileInput.files;

//     if (files.length > 0) {
//         uploadedFilePath = URL.createObjectURL(files[0]); // Store the uploaded image path
//         simulateProcessing(files, 0);
//     }
// }

// document.addEventListener("DOMContentLoaded", function () {
//     // Retrieve the uploaded image path from the query parameter
//     const uploadedFilePath = getParameterByName('uploadedFilePath');

//     // Update the 'resultImage' element with the uploaded image
//     const resultImage = document.getElementById('resultImage');

//     if (resultImage) {
//         resultImage.src = uploadedFilePath;
//     }
// });

function displayLoadingBar() {
    const loadingBar = document.getElementById('loadingBar');
    loadingBar.style.width = '0%';
    loadingBar.style.display = 'block';

    let width = 0;
    const interval = setInterval(() => {
        width += 10;
        loadingBar.style.width = width + '%';
        if (width >= 100) {
            clearInterval(interval);
        }
    }, 200);
}

function hideLoadingBar() {
    const loadingBar = document.getElementById('loadingBar');
    loadingBar.style.display = 'none';
    loadingBar.style.width = '0%';
}
// Function to retrieve URL parameters
function getParameterByName(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

function simulateProcessing(files, index) {
    if (index < files.length) {
        const currentFile = files[index];

        setTimeout(() => {
            console.log('Processing completed for:', currentFile.name);

            if (index === files.length - 1) {
                hideLoadingBar();
                showResultsButton();
            }

            simulateProcessing(files, index + 1);
        }, 2000); // Simulated processing time (adjust as needed)
    }
}

// function showResultsButton() {
//     const resultsButton = document.createElement('button');
//     resultsButton.textContent = 'See Results';
//     resultsButton.id = 'resultsButton';
//     resultsButton.addEventListener('click', redirectToResults);

//     // Pass the uploaded image path as a query parameter
//     resultsButton.dataset.uploadedFilePath = uploadedFilePath;

//     const container = document.getElementById('container');
//     container.appendChild(resultsButton);

//     // Apply CSS styles for the fade-in effect
//     resultsButton.style.opacity = '0';
//     resultsButton.style.transition = 'opacity 0.5s';

//     // Use setTimeout to delay the appearance for the fade-in effect
//     setTimeout(() => {
//         resultsButton.style.opacity = '1';
//     }, 100);
// }

// function redirectToResults() {
//     // Retrieve the uploaded image path from the data attribute
//     const uploadedFilePath = document.getElementById('resultsButton').dataset.uploadedFilePath;

//     // Redirect to results.html with the uploaded image path as a query parameter
//     window.location.href = `results.html?uploadedFilePath=${encodeURIComponent(uploadedFilePath)}`;
// }