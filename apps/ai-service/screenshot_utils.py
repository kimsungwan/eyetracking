import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def capture_screenshot(url: str, output_path: str):
    """
    Captures a full-page screenshot of the given URL and saves it to output_path.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(2)  # Wait for page to load
        
        # Get full page height
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, total_height)
        time.sleep(1) # Wait for resize
        
        driver.save_screenshot(output_path)
        print(f"Screenshot saved to {output_path}")
        return True
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return False
    finally:
        driver.quit()
