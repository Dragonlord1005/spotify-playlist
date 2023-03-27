import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
username = os.getenv('SPOTIPY_USERNAME')

# Set up Spotify API authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope='playlist-modify-public, playlist-modify-private, user-library-read, user-library-modify'))


# Retrieve all r/Maliciouscompliance episodes
show_id = 'spotify:show:3hJo9o8qFqrblXu1Plkv8L'
episode_uris = []

for offset in range(501):
    results = sp.show_episodes(show_id=show_id, market='US', limit=50, offset=offset)
    
    # Print out what offset we're on
    print("We're on offset {}".format(offset))

    # Filter out non r/Maliciouscompliance episodes and retrieve their URIs
    for item in results['items']:
        if item['name'].startswith('r/Maliciouscompliance'):
            episode_uris.append(item['uri'])

# Check if playlist already exists, and create it if it doesn't
playlist_name = 'r/MaliciousCompliance Episodes'
existing_playlists = sp.user_playlists(username)
playlist_exists = False
for playlist in existing_playlists['items']:
    if playlist['name'] == playlist_name:
        playlist_id = playlist['id']
        playlist_exists = True
        break
if not playlist_exists:
    new_playlist = sp.user_playlist_create(username, playlist_name, public=True)
    playlist_id = new_playlist['id']

# Add episodes to playlist, without creating duplicates
existing_tracks = sp.playlist_tracks(playlist_id)['items']
existing_track_uris = [track['track']['uri'] for track in existing_tracks]
new_track_uris = [episode_uri for episode_uri in episode_uris if episode_uri not in existing_track_uris]
if new_track_uris:
    # Split new_track_uris into batches of up to 100 and add each batch individually
    for i in range(0, len(new_track_uris), 100):
        batch = new_track_uris[i:i+100]
        sp.playlist_add_items(playlist_id, batch)

# Sort playlist by oldest to newest
# TODO: Fix not sorting correctly, or at all for that matter
# Sort playlist by oldest to newest
playlist_length = len(existing_tracks) + len(new_track_uris)
if playlist_length > 1:
    sp.playlist_reorder_items(playlist_id, range_start=0, insert_before=1, range_length=playlist_length)
