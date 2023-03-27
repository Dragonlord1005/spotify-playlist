import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up Spotify API authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='your_client_id',
                                               client_secret='your_client_secret',
                                               redirect_uri='your_redirect_uri',
                                               scope='playlist-modify-public'))

# Set up query to retrieve all rSlash episodes starting with r/maliciouscompliance
query = 'rSlash maliciouscompliance'

# Search for tracks using query
results = sp.search(q=query, type='track')

# Extract track IDs from search results
track_ids = []
for item in results['tracks']['items']:
    track_ids.append(item['id'])

# Check if playlist already exists, and create it if it doesn't
playlist_name = 'rSlash episodes (starting with r/maliciouscompliance)'
existing_playlists = sp.user_playlists('your_spotify_username')
playlist_exists = False
for playlist in existing_playlists['items']:
    if playlist['name'] == playlist_name:
        playlist_id = playlist['id']
        playlist_exists = True
        break
if not playlist_exists:
    new_playlist = sp.user_playlist_create('your_spotify_username', playlist_name, public=True)
    playlist_id = new_playlist['id']

# Add tracks to playlist, without creating duplicates
existing_tracks = sp.playlist_tracks(playlist_id)['items']
existing_track_ids = [track['track']['id'] for track in existing_tracks]
new_track_ids = [track_id for track_id in track_ids if track_id not in existing_track_ids]
if new_track_ids:
    sp.playlist_add_items(playlist_id, new_track_ids)
    
# Sort playlist by youngest to oldest
sp.playlist_reorder_tracks(playlist_id, [track['track']['id'] for track in existing_tracks][::-1])