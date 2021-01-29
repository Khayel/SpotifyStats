import json
from flask import Flask, request, redirect, g, render_template
import requests

client_id = '36567bdba090467cbc6b6654ffbac5e6'
client_secret = '2efa5e6294444b8bb6cbe0b5d7604a5a'
auth_payload = {
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

def spotifyAPI(auth_header, reqString, param,reqType='GET'):
    print("in SPOOTIFYAPI")
    if reqType not in ['GET','POST']:
        raise ValueError("reqType must be HTTP request type (get,post")
    rString = '{}/{}'.format(SPOTIFY_API_URL,reqString)
    if reqType == 'GET':
        print(auth_header)
        apiResponse = requests.get(rString, headers=auth_header)
        return json.loads(apiResponse.text)


@app.route("/")
def home():
    return render_template('index.html')
@app.route("/login")
def index():
    # Auth Step 1: Authorization creates url string with authorizatioon payload
    url_args = "&".join(["{}={}".format(key, val) for key, val in auth_payload.items()])
    auth_url = "{}/?{}".format(SPOTIFYAUTH_URL, url_args)
   
    return redirect(auth_url) #afterpermissions accepted spotify gives redirect URI

#Redirect URI calls callback with auth code and state
@app.route("/callback/q")
def callback():
    #use code,redirect uri(only for validation), and client id and secret
    #to get Access and refresh token
    #permission denied or error
    
    payload = {
        "grant_type": "authorization_code",
        "code": str(request.args['code']),
        "redirect_uri": 'http://localhost:5000/callback/q',
        'client_id': client_id,
        'client_secret': client_secret
    }
    r = requests.post(SPOTIFY_TOKEN_URL,payload)
    print(r)
    response_data = json.loads(r.text)


    #create Auth header for every request
    access_token = response_data['access_token']
    #print(access_token)
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    
    #-----AUTH FINISHED
    result = spotifyAPI(auth_header,reqString='me',param='')
    print(result)


    #user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)

    #profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    #profile_data = json.loads(profile_response.text)
    #playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    #playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    #playlist_data = json.loads(playlists_response.text)
    #display_arr = [profile_data] + playlist_data["items"]
    return render_template("loginSplash.html", sorted_array=result)

    

if __name__ == "__main__":
    app.run(debug=True )