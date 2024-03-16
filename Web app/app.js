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
        }, 2000); // Simulated processing time
    }
}

