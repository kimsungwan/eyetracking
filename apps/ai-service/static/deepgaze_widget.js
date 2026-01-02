class DeepGazeWidget {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`DeepGazeWidget: Container #${containerId} not found.`);
            return;
        }
        this.injectStyles();
        this.render();

        // Initialize Report Widget
        // We pass a callback for when the user clicks "Analyze Another"
        this.reportWidget = new ReportWidget('dg-report-actions', () => this.reset());

        this.attachEvents();
    }

    injectStyles() {
        if (document.getElementById('deepgaze-widget-styles')) return;
        const style = document.createElement('style');
        style.id = 'deepgaze-widget-styles';
        style.textContent = `
            .dg-upload-container {
                border: 3px dashed #e3dfed;
                border-radius: 20px;
                padding: 60px 20px;
                text-align: center;
                background: #fff;
                transition: all 0.3s ease;
                cursor: pointer;
                margin-bottom: 30px;
            }
            .dg-upload-container:hover, .dg-upload-container.dragover {
                border-color: #8d81ac;
                background: #f4f4f4;
            }
            .dg-icon {
                font-size: 48px;
                color: #8d81ac;
                margin-bottom: 20px;
            }
            .dg-loading {
                text-align: center;
                padding: 40px;
            }
            .dg-spinner {
                width: 50px;
                height: 50px;
                border: 4px solid #f3f3f3;
                border-top: 4px solid #8d81ac;
                border-radius: 50%;
                animation: dg-spin 1s linear infinite;
                margin: 0 auto 20px;
            }
            @keyframes dg-spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            .dg-results {
                display: flex;
                flex-wrap: wrap;
                gap: 30px;
                justify-content: center;
                margin-top: 40px;
            }
            .dg-card {
                background: #fff;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.05);
                flex: 1;
                min-width: 300px;
                max-width: 500px;
            }
            .dg-card h3 {
                margin-top: 0;
                color: #635C73;
                font-size: 1.8rem;
                margin-bottom: 15px;
            }
            .dg-card img {
                width: 100%;
                border-radius: 5px;
                display: block;
            }
            .dg-actions-container {
                margin-top: 40px;
                text-align: center;
            }
        `;
        document.head.appendChild(style);
    }

    render() {
        this.container.innerHTML = `
            <div class="dg-widget-wrapper">
                <div class="dg-upload-container" id="dg-drop-zone">
                    <input type="file" id="dg-file-input" accept="image/*" hidden>
                    <div class="dg-upload-content">
                        <div class="dg-icon"><i class="fa fa-cloud-upload"></i></div>
                        <h3 style="color: #635C73; font-weight: bold;">Drag & Drop UI Design</h3>
                        <p style="color: #848e97;">or click to browse (JPG, PNG)</p>
                    </div>
                </div>

                <div class="dg-loading" id="dg-loading" style="display: none;">
                    <div class="dg-spinner"></div>
                    <p style="font-size: 1.6rem; color: #635C73;">Running Uvolution AI Model...</p>
                    <p style="color: #848e97;">Predicting human attention patterns</p>
                </div>

                <div class="dg-results" id="dg-results" style="display: none;">
                    <div class="dg-card">
                        <h3>Original Design</h3>
                        <img id="dg-original-img" src="" alt="Original">
                    </div>
                    <div class="dg-card">
                        <h3>Attention Heatmap</h3>
                        <img id="dg-saliency-img" src="" alt="Saliency Map">
                    </div>
                </div>
                
                <!-- Container for Report Widget -->
                <div id="dg-report-actions" class="dg-actions-container"></div>
            </div>
        `;
    }

    attachEvents() {
        const dropZone = this.container.querySelector('#dg-drop-zone');
        const fileInput = this.container.querySelector('#dg-file-input');

        dropZone.addEventListener('click', () => fileInput.click());

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
        });

        dropZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) this.handleFiles(files[0]);
        }, false);

        fileInput.addEventListener('change', (e) => {
            if (fileInput.files.length > 0) this.handleFiles(fileInput.files[0]);
        });
    }

    handleFiles(file) {
        this.uploadFile(file);
    }

    async uploadFile(file) {
        const loading = this.container.querySelector('#dg-loading');
        const dropZone = this.container.querySelector('#dg-drop-zone');
        const results = this.container.querySelector('#dg-results');

        const originalImg = this.container.querySelector('#dg-original-img');
        const saliencyImg = this.container.querySelector('#dg-saliency-img');

        dropZone.style.display = 'none';
        loading.style.display = 'block';
        results.style.display = 'none';
        this.reportWidget.hide(); // Hide buttons

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Upload failed');

            const data = await response.json();

            // Check for error FIRST to prevent 404s on undefined paths
            if (data.error) {
                console.error("Server reported error:", data.error);
                alert("Analysis failed: " + data.error);
                this.reportWidget.show("#");
                loading.style.display = 'none';
                return; // Stop execution
            }

            const timestamp = new Date().getTime();

            // Only set sources if data exists
            if (data.original_image) originalImg.src = `/${data.original_image}?t=${timestamp}`;
            if (data.saliency_map) saliencyImg.src = `/${data.saliency_map}?t=${timestamp}`;

            // Show results
            loading.style.display = 'none';
            results.style.display = 'flex';

            // Show Report Widget (Buttons)
            if (data.report) {
                this.reportWidget.show(data.report);
            } else {
                console.error("Report path missing in response:", data);
                alert("Analysis complete, but report link is missing. Please check server logs.");
                this.reportWidget.show("#"); // Fallback
            }

        } catch (error) {
            console.error(error);
            alert('Error processing image');
            this.reset();
        }
    }

    reset() {
        this.container.querySelector('#dg-drop-zone').style.display = 'block';
        this.container.querySelector('#dg-loading').style.display = 'none';
        this.container.querySelector('#dg-results').style.display = 'none';
        this.reportWidget.hide();
        this.container.querySelector('#dg-file-input').value = '';
    }
}

window.DeepGazeWidget = DeepGazeWidget;
