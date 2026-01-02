import os
import requests
import zipfile
import io

def download_file(url, filename):
    print(f"Downloading {filename} from {url}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {filename} successfully.")
        return True
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
        return False

def main():
    datasets_dir = os.path.dirname(os.path.abspath(__file__))
    
    # UEyes Dataset (Zenodo)
    ueyes_url = "https://zenodo.org/record/8010312/files/UEyes.zip?download=1"
    ueyes_zip = os.path.join(datasets_dir, "UEyes.zip")
    
    if not os.path.exists(ueyes_zip):
        if download_file(ueyes_url, ueyes_zip):
            print("Extracting UEyes.zip...")
            try:
                with zipfile.ZipFile(ueyes_zip, 'r') as zip_ref:
                    zip_ref.extractall(datasets_dir)
                print("Extracted UEyes.")
            except Exception as e:
                print(f"Failed to extract: {e}")
    else:
        print("UEyes.zip already exists.")

    # Placeholder for others (often require login or form submission)
    print("\nNote: WIC640 and Imp1k often require manual form submission or have complex direct links.")
    print("Please visit the links in README.md for manual download if needed.")

if __name__ == "__main__":
    main()
