const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const actions = document.getElementById('actions');
const originalImg = document.getElementById('original-img');
const saliencyImg = document.getElementById('saliency-img');
const downloadBtn = document.getElementById('download-report-btn');
const resetBtn = document.getElementById('reset-btn');

// Drag & Drop
dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#6366f1';
});

dropZone.addEventListener('dragleave', () => {
    dropZone.style.borderColor = '#94a3b8';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#94a3b8';
    if (e.dataTransfer.files.length) {
        handleFile(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length) {
        handleFile(fileInput.files[0]);
    }
});

function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please upload an image file.');
        return;
    }

    // Show loading
    dropZone.style.display = 'none';
    loading.style.display = 'block';
    results.style.display = 'none';
    actions.style.display = 'none';

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                resetView();
                return;
            }

            // Show results
            loading.style.display = 'none';
            results.style.display = 'flex';
            actions.style.display = 'flex';

            // Update images (add timestamp to prevent caching)
            originalImg.src = '/' + data.original_image + '?t=' + new Date().getTime();
            saliencyImg.src = '/' + data.saliency_map + '?t=' + new Date().getTime();

            // Update download link
            downloadBtn.href = '/' + data.report;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during processing.');
            resetView();
        });
}

resetBtn.addEventListener('click', resetView);

function resetView() {
    dropZone.style.display = 'block';
    loading.style.display = 'none';
    results.style.display = 'none';
    actions.style.display = 'none';
    fileInput.value = '';
}
