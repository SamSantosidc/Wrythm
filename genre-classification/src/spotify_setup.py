import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# Carregar variáveis do arquivo .env
load_dotenv()

def create_spotify_client():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError("Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET in env vars")

    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )

    return Spotify(auth_manager=auth_manager, requests_timeout=10, retries=2)

# Instância criada automaticamente ao importar
sp = create_spotify_client()
