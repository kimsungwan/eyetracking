class ReportWidget {
    constructor(containerId, onReset) {
        this.container = document.getElementById(containerId);
        this.onReset = onReset;
        if (!this.container) return;

        this.render();
        this.attachEvents();
    }

    render() {
        this.container.innerHTML = `
            <div class="dg-actions-wrapper" style="display: none;">
                <a id="rw-download-btn" href="#" target="_blank" class="btn btn-primary rounded">
                    <i class="fa fa-download"></i> Download Full Report
                </a>
                <button id="rw-reset-btn" class="btn btn-default rounded">
                    Analyze Another
                </button>
            </div>
        `;
    }

    attachEvents() {
        const resetBtn = this.container.querySelector('#rw-reset-btn');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                this.hide();
                if (this.onReset) this.onReset();
            });
        }
    }

    show(reportUrl) {
        const wrapper = this.container.querySelector('.dg-actions-wrapper');
        const downloadBtn = this.container.querySelector('#rw-download-btn');

        if (wrapper && downloadBtn) {
            // Fix: Ensure the URL is absolute or correctly relative
            // If reportUrl already starts with /, don't add another one
            const finalUrl = reportUrl.startsWith('/') ? reportUrl : `/${reportUrl}`;

            downloadBtn.href = finalUrl;
            wrapper.style.display = 'block';

            // Optional: Auto-click or focus
            downloadBtn.focus();
        }
    }

    hide() {
        const wrapper = this.container.querySelector('.dg-actions-wrapper');
        if (wrapper) {
            wrapper.style.display = 'none';
        }
    }
}

window.ReportWidget = ReportWidget;
