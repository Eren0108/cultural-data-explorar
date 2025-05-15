import os
import pandas as pd
import requests
from pathlib import Path

def download_image(url, save_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    # Create directories if they don't exist
    for dir_name in ['assets/images/heritage', 'assets/images/events', 'assets/images/art']:
        Path(dir_name).mkdir(parents=True, exist_ok=True)

    # Read image URLs
    df = pd.read_csv('data/image_urls.csv')
    
    # Download images for each category
    for _, row in df.iterrows():
        if row['Type'] == 'heritage':
            save_path = f"assets/images/heritage/{row['Name'].lower().replace(' ', '_')}.jpg"
        elif row['Type'] == 'event':
            save_path = f"assets/images/events/{row['Name'].lower().replace(' ', '_')}.jpg"
        else:  # art
            save_path = f"assets/images/art/{row['Name'].lower().replace(' ', '_')}.jpg"
        
        if not os.path.exists(save_path):
            print(f"Downloading {row['Name']}...")
            success = download_image(row['Image_URL'], save_path)
            if success:
                print(f"Successfully downloaded {row['Name']}")
            else:
                print(f"Failed to download {row['Name']}")

if __name__ == "__main__":
    main()
    print("Download process completed!") 