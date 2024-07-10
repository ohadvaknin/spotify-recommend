import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Authenticate with Spotify API
CLIENT_ID = '8877c0f20ea448e78c6e06f05fe61b40'
CLIENT_SECRET = '42bda3a602dd4ffea319ed344e74c7dd'
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_artist_id(artist_name):
    result = sp.search(q='artist:' + artist_name, type='artist')
    return result['artists']['items'][0]['id'] if result['artists']['items'] else None

def get_artist_data(artist_id):
    artist = sp.artist(artist_id)
    return {
        'name': artist['name'],
        'genres': artist['genres']
    }

def get_related_artists(artist_id):
    results = sp.artist_related_artists(artist_id)
    return [artist['id'] for artist in results['artists']]

def build_artist_network(seed_artist_ids, depth):
    artist_data = {}
    edges = []
    current_depth_artists = {1: seed_artist_ids}

    def add_artist(artist_id):
        artist_info = get_artist_data(artist_id)
        artist_data[artist_id] = artist_info
        related_artists = get_related_artists(artist_id)
        for related_artist_id in related_artists:
            edges.append((artist_id, related_artist_id))
            next_depth_artists.add(related_artist_id)
        #print(f"Added {artist_info['name']}")

    for current_depth in range(1, depth + 1):
        next_depth_artists = set()
        for artist_id in current_depth_artists.get(current_depth, []):
            if artist_id not in artist_data:
                add_artist(artist_id)
        current_depth_artists[current_depth + 1] = list(next_depth_artists)

    return artist_data, edges

def analyze_network(seed_artist_ids):
    artist_data, edges = build_artist_network(seed_artist_ids, depth=2)
    artist_df = pd.DataFrame.from_dict(artist_data, orient='index')
    G = nx.Graph()

    for artist_id, info in artist_data.items():
        G.add_node(artist_id, name=info['name'])

    for edge in edges:
        G.add_edge(*edge)

    centrality = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)

    artist_df['centrality'] = artist_df.index.map(centrality)
    artist_df['betweenness'] = artist_df.index.map(betweenness)
    artist_df['closeness'] = artist_df.index.map(closeness)

    return artist_df, G

def recommend_artists(artist_df, G, seed_artist_ids, top_n=5):
    artist_df['combined_score'] = artist_df['centrality'] + artist_df['betweenness'] + artist_df['closeness']
    recommendations = artist_df[~artist_df.index.isin(seed_artist_ids)]
    recommendations = recommendations.sort_values(by='combined_score', ascending=False)
    return recommendations.head(top_n)

def get_recommendations(artist1, artist2, artist3):
    seed_artist_ids = [get_artist_id(artist1), get_artist_id(artist2), get_artist_id(artist3)]
    artist_df, G = analyze_network(seed_artist_ids)
    recommended_artists = recommend_artists(artist_df, G, seed_artist_ids)
    return recommended_artists['name'].tolist()
