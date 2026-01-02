const urls = [
    'http://localhost:3000/en',
    'http://localhost:3000/en/pricing',
    'http://localhost:3000/en/science',
    'http://localhost:3000/en/analyze'
];

async function checkUrls() {
    for (const url of urls) {
        try {
            const response = await fetch(url);
            console.log(`Checking ${url}: Status ${response.status}`);
        } catch (error) {
            console.error(`Error checking ${url}:`, error.message);
        }
    }
}

checkUrls();
