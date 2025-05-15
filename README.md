# Cultural Data Explorer

An interactive web application built with Streamlit to explore cultural heritage sites, events, and art forms.

## Features

- Interactive maps showing heritage sites
- Cultural events timeline and details
- Art forms exploration and visualization
- Data filtering and search capabilities
- Image galleries for each category

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Project Structure

- `app.py`: Main application file
- `pages/`: Contains individual pages for Heritage Sites, Cultural Events, and Art Forms
- `data/`: CSV files containing cultural data
- `assets/`: Images and other static resources
- `download_images.py`: Utility script for downloading images

## Note
Make sure to update the image URLs in the data files with valid sources before running the image download script. 