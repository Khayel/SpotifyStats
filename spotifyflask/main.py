import json
from flask import Flask, request, redirect, render_template, url_for,session
from flask_restful import Resource, Api
import requests
import os

client_id = CLIENT_ID
client_secret = CLIENT_SECRET 
auth_payload = {
    'client_id': client_id,
    'response_type': 'code',
    'redirect_uri': 'http://spotifystats-flask.herokuapp.com/callback/q',
    'scope': 'playlist-modify-public user-top-read playlist-modify-private user-read-email user-read-private'
}
SPOTIFYAUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)



class topTrackOptions(Resource):
    def get(self):
        """Returns list of top Artists
        """
        return spotifyAPI('me/top/tracks', 'time_range={}'.format(request.args['time_range']))

class topArtistOptions(Resource):
    def get(self):
        """Returns list of top Artists
        """
        return spotifyAPI('me/top/artists','time_range={}'.format(request.args['time_range']))


class createTopTrackPlaylist(Resource):
    """
    Create playlist POST https://api.spotify.com/v1/users/{user_id}/playlists 
    Add Tracks to playlist POST https://api.spotify.com/v1/playlists/{playlist_id}/tracks?
    """
    def post(self):
        print("HERE")
        auth_header = {"Authorization": "Bearer {}".format(session['auth_token'])}
        getUserID = spotifyAPI('me','')   
        user_id = getUserID['id']

        time_range = request.form.get('time_range')
        payload = {
            "name": "TopTracks - {}".format(time_range),
            "description": "My Top Tracks in {}".format(time_range),
            "public": "false"
            }
        newPlayListRequest = '{}/users/{}/playlists'.format(SPOTIFY_API_URL, user_id)
        resp = requests.post(newPlayListRequest, data=json.dumps(payload), header=auth_header)
        resp = resp.json()
        playlist_Id = resp['id']
        print("Created PlayList with ID:", playlist_Id)

        trackList = spotifyAPI('me/top/tracks', 'time_range={}'.format(time_range))
        payload = {
        "uris":[track['uri'] for track in trackList['items']]
        }
        add_tracks = requests.post('{}/playlists/{}/tracks'.format(SPOTIFY_API_URL, playlist_Id), data=json.dumps(payload), headers=auth_header)
        return add_tracks.json()

app = Flask(__name__)
app.secret_key = os.urandom(24)
api = Api(app)

api.add_resource(topTrackOptions, '/api/dateRange/tracks')
api.add_resource(topArtistOptions, '/api/dateRange/artists')
api.add_resource(createTopTrackPlaylist, '/api/createPlaylist')

def spotifyAPI(reqString, param, reqType='GET'):
    """Helper function for calling Spotify API"""

    auth_header = {"Authorization": "Bearer {}".format(session['auth_token'])}
    print(auth_header)
    rString = '{}/{}?{}'.format(SPOTIFY_API_URL, reqString, param)
    if reqType == 'GET':
        print(" SPOTIFY API REQUEST: ", rString)
        apiResponse = requests.get(rString, headers=auth_header)
        print("RESULT: ", apiResponse)
        return apiResponse.json()

@app.route("/home")
def home():
    return render_template('home.html')

@ app.route("/topTracks")
def topTracks():
    return render_template("tracks.html", topTracks=topTracks)

@ app.route("/topArtists")
def topArtists():
    topArtists = spotifyAPI('me/top/artists', 'time_range=short_term')
    return render_template("artists.html", topArtists=topArtists)


@ app.route("/")
def index():
    #Landing Page
    return render_template('intro.html')


@app.route("/login")
def login():
    # Auth Step 1: Authorization creates url string with authorizatioon payload
    url_args = "&".join(["{}={}".format(key, val)
                         for key, val in auth_payload.items()])
    auth_url = "{}/?{}".format(SPOTIFYAUTH_URL, url_args)

    # afterpermissions accepted spotify gives redirect URI
    return redirect(auth_url)

#callback url set in Spotify API Dashboard
#Authorization code flow
# use code,redirect uri(only for validation), and client id and secret
# to get Access and refresh token
# permission denied or error
@ app.route("/callback/q")
def callback():   
    payload = {
        "grant_type": "authorization_code",
        "code": str(request.args['code']),
        "redirect_uri": 'http://spotifystats-flask.herokuapp.com/callback/q',
        'client_id': client_id,
        'client_secret': client_secret
    }
    r = requests.post(SPOTIFY_TOKEN_URL, payload)
    response_data = json.loads(r.text)
    # create Auth header for every request
    access_token = response_data['access_token']
    
    auth_token = access_token
    session['auth_token'] = auth_token
    # auth_header = {"Authorization": "Bearer {}".format(access_token)}

    # -----AUTH FINISHED
    print("Success Authorization")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
