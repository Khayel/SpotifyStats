import json
from flask import Flask, request, redirect, g, render_template, url_for
from flask_restful import Resource, Api
import requests

client_id = '36567bdba090467cbc6b6654ffbac5e6'
client_secret = '2efa5e6294444b8bb6cbe0b5d7604a5a'
auth_payload = {
    'client_id': client_id,
    'response_type': 'code',
    'redirect_uri': 'http://localhost:5000/callback/q',
    'scope': 'playlist-modify-public user-top-read playlist-modify-private streaming user-read-email user-read-private'
}
SPOTIFYAUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


class topTrackOptions(Resource):
    def get(self):
        return spotifyAPI('me/top/tracks', 'time_range={}'.format(request.args['time_range']))

class topArtistOptions(Resource):
    def get(self):
        return spotifyAPI('me/top/artists','time_range={}'.format(request.args['time_range']))

app = Flask(__name__)
api = Api(app)

api.add_resource(topTrackOptions, '/api/dateRange/tracks')
api.add_resource(topArtistOptions, '/api/dateRange/artists')



def spotifyAPI(reqString, param, reqType='GET'):
    print("in SPOOTIFYAPI")
    rString = '{}/{}?{}'.format(SPOTIFY_API_URL, reqString, param)
    if reqType == 'GET':
        print("API REQUEST: ", rString)
        apiResponse = requests.get(rString, headers=auth_header)
        print("RESULT: ", apiResponse)
        return apiResponse.json()


@ app.route("/dashboard")
def dashboard():
    top3Track = spotifyAPI('me/top/tracks', 'limit=3&time_range=long_term')
    top3Artist = spotifyAPI('me/top/artists', 'limit=3&time_range=long_term')
    return render_template('index.html', top3Track=top3Track, top3Artist=top3Artist)

@app.route("/home")
def home():
    return render_template('home.html')

@ app.route("/topTracks")
def topTracks():
    topTracks = spotifyAPI('me/top/tracks', 'time_range=short_term')
    return render_template("tracks.html", topTracks=topTracks)

@ app.route("/topArtists")
def topArtists():
    topArtists = spotifyAPI('me/top/artists', 'time_range=short_term')
    return render_template("artists.html", topArtists=topArtists)

@ app.route("/")
def index():
    return render_template('intro.html')


@app.route("/login")
def login():
    # Auth Step 1: Authorization creates url string with authorizatioon payload
    url_args = "&".join(["{}={}".format(key, val)
                         for key, val in auth_payload.items()])
    auth_url = "{}/?{}".format(SPOTIFYAUTH_URL, url_args)

    # afterpermissions accepted spotify gives redirect URI
    return redirect(auth_url)

# Redirect URI calls callback with auth code and state

#callback url from Spotify API
#Authorization code flow
@ app.route("/callback/q")
def callback():
    # use code,redirect uri(only for validation), and client id and secret
    # to get Access and refresh token
    # permission denied or error
    print("CALLBACK CALLED")
    payload = {
        "grant_type": "authorization_code",
        "code": str(request.args['code']),
        "redirect_uri": 'http://localhost:5000/callback/q',
        'client_id': client_id,
        'client_secret': client_secret
    }
    r = requests.post(SPOTIFY_TOKEN_URL, payload)
    response_data = json.loads(r.text)
    # create Auth header for every request
    try:
        access_token = response_data['access_token']
    except:
        return "NOACCESS TOKEN"
    global authToken
    authToken = access_token
    global auth_header
    auth_header = {"Authorization": "Bearer {}".format(access_token)}

    # -----AUTH FINISHED
    print("Success Authorization")
    return redirect(url_for('home'))


@ app.route('/playback')
def playback():
    try:
        if authToken != '':
            return render_template('playback.html', authToken=authToken)

    except:
        return "login first -> redirectto logon pahge"

if __name__ == "__main__":
    app.run(debug=True)
