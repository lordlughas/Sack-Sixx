import requests
from flask import Flask, render_template, request

app = Flask(__name__)

SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"
SPOTIFY_ACCESS_TOKEN = "YOUR_SPOTIFY_ACCESS_TOKEN"  # Replace with your Spotify access token


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    artist = request.form["artist"]

    # Fetch artist information
    artist_info = fetch_artist_info(artist)

    if artist_info:
        artist_name = artist_info["name"]
        artist_image_url = artist_info["images"][0]["url"]

        # Fetch track recommendations
        track_recommendations = fetch_track_recommendations(artist)

        return render_template(
            "recommendations.html",
            artist=artist_name,
            artist_image=artist_image_url,
            tracks=track_recommendations,
        )
    else:
        error_message = "Unable to fetch artist information."
        return render_template("recommendations.html", error_message=error_message)


def fetch_artist_info(artist):
    headers = {
        "Authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"
    }
    params = {
        "q": artist,
        "type": "artist",
        "limit": 1
    }
    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/search",
        headers=headers,
        params=params
    )
    data = response.json()

    if "artists" in data and "items" in data["artists"]:
        items = data["artists"]["items"]
        if items:
            return items[0]

    return None


def fetch_track_recommendations(artist):
    headers = {
        "Authorization": f"Bearer {SPOTIFY_ACCESS_TOKEN}"
    }
    params = {
        "seed_artists": artist,
        "limit": 10
    }
    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/recommendations",
        headers=headers,
        params=params
    )
    data = response.json()

    if "tracks" in data:
        return data["tracks"]

    return None


if __name__ == "__main__":
    app.run(debug=True)

