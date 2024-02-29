function handleUpload() {
    displayLoadingBar();
    const fileInput = document.getElementById('uploadInput');
    const files = fileInput.files;

    if (files.length > 0) {
        simulateProcessing(files, 0);
    }
}

function handleDrop(event) {
    displayLoadingBar();
    event.preventDefault();
    const droppedFiles = event.dataTransfer.files;

    if (droppedFiles.length > 0) {
        simulateProcessing(droppedFiles, 0);
    }
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

function showResultsButton() {
    const resultsButton = document.createElement('button');
    resultsButton.textContent = 'See Results';
    resultsButton.id = 'resultsButton';
    resultsButton.addEventListener('click', redirectToResults);

    const container = document.getElementById('container');
    container.appendChild(resultsButton);

    // Apply CSS styles for the fade-in effect
    resultsButton.style.opacity = '0';
    resultsButton.style.transition = 'opacity 0.5s';

    // Use setTimeout to delay the appearance for the fade-in effect
    setTimeout(() => {
        resultsButton.style.opacity = '1';
    }, 100);
}

function redirectToResults() {
    window.location.href = 'results.html';
}

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