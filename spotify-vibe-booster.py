import spotipy
from spotipy.oauth2 import SpotifyOAuth


def add_liked_songs_to_playlist(username, playlist_name):
    # Replace these values with your Spotify developer dashboard credentials in settings section and desired playlist information
    client_id = "your_client_id"
    client_secret = "your_client_secret"
    # You can skip editing this part
    redirect_uri = "http://localhost:8888/callback"

    # Spotify API authentication
    scope = "user-library-read playlist-modify-public"
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            username=username,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
        )
    )

    # Get user's liked songs with pagination
    results = sp.current_user_saved_tracks()
    tracks = results["items"]
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    # Get the authenticated user's ID
    user_id = sp.me()["id"]

    # Create a new playlist for the authenticated user
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    playlist_id = playlist["id"]

    # Add liked songs to the new playlist in batches (max 100 tracks per request)
    batch_size = 100
    for i in range(0, len(tracks), batch_size):
        batch_track_uris = [
            track["track"]["uri"] for track in tracks[i : i + batch_size]
        ]
        sp.playlist_add_items(playlist_id, batch_track_uris)

    print(f"All liked songs added to the playlist '{playlist_name}'.")


if __name__ == "__main__":
    # Replace with your Spotify username and desired playlist name
    spotify_username = "your_spotify_username"
    playlist_name = "spotify-vibe-booster"

    add_liked_songs_to_playlist(spotify_username, playlist_name)
