// Features Section Loader
// Dynamically loads the features section from an external HTML file
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

    function loadFeaturesSection() {
        var placeholder = document.getElementById('features-placeholder');
        if (!placeholder) {
            console.warn('Features section placeholder not found');
            return;
        }

        var lang = getCurrentLanguage();
        var filename = lang === 'en'
            ? '/static/features-section.html'
            : '/static/features-section_' + lang + '.html';

        // Fetch the features section HTML
        fetch(filename)
            .then(function (response) {
                if (!response.ok) {
                    throw new Error('Failed to load features section: ' + response.status);
                }
                return response.text();
            })
            .then(function (html) {
                placeholder.outerHTML = html;
            })
            .catch(function (error) {
                console.error('Error loading features section:', error);
                // Fallback: create empty features section if load fails
                placeholder.innerHTML = '<section class="area" id="features"><div class="container"><p>Features section could not be loaded.</p></div></section>';
            });
    }

    // Load on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadFeaturesSection);
    } else {
        loadFeaturesSection();
    }
})();
