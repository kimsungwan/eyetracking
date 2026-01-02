// Science Section Loader
// Dynamically loads the science section from an external HTML file
(function () {
    'use strict';

    function getCurrentLanguage() {
        // Get current path to determine language
        var path = window.location.pathname;
        if (path === '/ko') return 'ko';
        if (path === '/cn') return 'cn';
        if (path === '/jp') return 'jp';
        return 'en'; // default to English
    }

    function loadScienceSection() {
        var placeholder = document.getElementById('science-placeholder');
        if (!placeholder) {
            console.warn('Science section placeholder not found');
            return;
        }

        var lang = getCurrentLanguage();
        var filename = lang === 'en'
            ? '/static/science-section.html'
            : '/static/science-section_' + lang + '.html';

        // Fetch the science section HTML
        fetch(filename)
            .then(function (response) {
                if (!response.ok) {
                    throw new Error('Failed to load science section: ' + response.status);
                }
                return response.text();
            })
            .then(function (html) {
                placeholder.outerHTML = html;
            })
            .catch(function (error) {
                console.error('Error loading science section:', error);
                // Fallback: create empty science section if load fails
                placeholder.innerHTML = '<section class="area" id="science"><div class="container"><p>Science section could not be loaded.</p></div></section>';
            });
    }

    // Load on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadScienceSection);
    } else {
        loadScienceSection();
    }
})();
