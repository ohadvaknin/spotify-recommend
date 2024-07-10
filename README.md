
# Spotify Artist Recommender

This is a Flask web application that recommends artists based on the similarity to three seed artists provided by the user. The recommendation is based on data retrieved from the Spotify API and network analysis performed using NetworkX.

## Project Structure

```
flask_app/
│
├── app.py                      # Main Flask application
├── artist_recommender.py       # Module for recommending artists
├── config.py                   # Configuration file for storing API credentials
├── requirements.txt            # List of dependencies
├── templates/
│   └── index.html              # HTML template for the web page
└── static/
    ├── script.js               # JavaScript for handling the loading spinner
    └── style.css               # CSS for styling the web page
```

## Features

- User-friendly web interface for inputting seed artists
- Recommendations based on network analysis and graph theory

## Prerequisites

- Python 3.x
- Pip (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ohadvaknin/spotify-recommender.git
cd spotify-recommender
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Setup

1. Modify the `config.py` file in the root directory and fill in your Spotify API credentials:

```python
# config.py
SPOTIPY_CLIENT_ID = 'your_spotify_client_id'
SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'
```

## Running the Application

To start the Flask application, run the following command:

```bash
python app.py
```

By default, the application will be accessible at `http://0.0.0.0:5000`.
