import json
from flask import Flask, request, redirect, g, render_template
import requests
#import base64

client_id = '36567bdba090467cbc6b6654ffbac5e6'
client_secret = '2efa5e6294444b8bb6cbe0b5d7604a5a'
payload = {
    'client_id': client_id,
    'response_type': 'code',
    'redirect_uri': 'http://localhost:5000/callback/q',
    'scope': 'playlist-modify-public playlist-modify-private'    
}
SPOTIFYAUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')
@app.route("/login")
def index():
    # Auth Step 1: Authorization creates url 
    url_args = "&".join(["{}={}".format(key, val) for key, val in payload.items()])
    auth_url = "{}/?{}".format(SPOTIFYAUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/callback/q")
def callback():
    print(request.args['code'])
    #encodedData = base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")
    #authorization_header_string = f"Authorization: Basic {encodedData}"
    payload = {
        "grant_type": "authorization_code",
        "code": str(request.args['code']),
        "redirect_uri": 'http://localhost:5000/callback/q',
        'client_id': client_id,
        'client_secret': client_secret
    }
    r = requests.post(SPOTIFY_TOKEN_URL,payload)
    response_data = json.loads(r.text)
    access_token = response_data['access_token']
    print(response_data['token_type'])
    print(response_data['scope'])
    print(response_data['expires_in'])
    print(response_data['refresh_token'])
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    playlist_data = json.loads(playlists_response.text)
    display_arr = [profile_data] + playlist_data["items"]
    return render_template("loginSplash.html", sorted_array=display_arr)

    

if __name__ == "__main__":
    app.run(debug=True )