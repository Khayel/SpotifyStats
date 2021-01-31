window.onSpotifyWebPlaybackSDKReady = () => {
    const token = 'BQAkbfI-xDxpo-qYE3G1hAapCx8YmwugaJbKjZ_7ReVaYsoSI326XIa4I1akJuLex8QTiZSXwtkMQS5j4aZU80stRlwu5uWWyXhNO50m_vMaxufuiEC-7tMkz9lCEUcsnazZag6-dkmxxW8Vth-IP1v4wd-lHnWD';
    const player = new Spotify.Player({
        name: 'Web Playback SDK Quick Start Player',
        getOAuthToken: cb => { cb(token); }
    });

    // Error handling
    player.addListener('initialization_error', ({ message }) => { console.error(message); });
    player.addListener('authentication_error', ({ message }) => { console.error(message); });
    player.addListener('account_error', ({ message }) => { console.error(message); });
    player.addListener('playback_error', ({ message }) => { console.error(message); });

    // Playback status updates
    player.addListener('player_state_changed', state => { console.log(state); });

    // Ready
    player.addListener('ready', ({ device_id }) => {
        console.log('Ready with Device ID', device_id);
    });

    // Not Ready
    player.addListener('not_ready', ({ device_id }) => {
        console.log('Device ID has gone offline', device_id);
    });

    // Connect to the player!
    player.connect();
};