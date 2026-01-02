// Pricing Section Loader
// Dynamically loads the pricing section from an external HTML file
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

    function loadPricingSection() {
        var placeholder = document.getElementById('pricing-placeholder');
        if (!placeholder) {
            console.warn('Pricing section placeholder not found');
            return;
        }

        var lang = getCurrentLanguage();
        var filename = lang === 'en'
            ? '/static/pricing-section.html'
            : '/static/pricing-section_' + lang + '.html';

        // Fetch the pricing section HTML
        fetch(filename)
            .then(function (response) {
                if (!response.ok) {
                    throw new Error('Failed to load pricing section: ' + response.status);
                }
                return response.text();
            })
            .then(function (html) {
                placeholder.outerHTML = html;
            })
            .catch(function (error) {
                console.error('Error loading pricing section:', error);
                // Fallback: create empty pricing section if load fails
                placeholder.innerHTML = '<section class="area" id="pricing"><div class="container"><p>Pricing section could not be loaded.</p></div></section>';
            });
    }

    // Load on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadPricingSection);
    } else {
        loadPricingSection();
    }
})();
