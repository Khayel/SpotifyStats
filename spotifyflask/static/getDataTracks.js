console.log("THIS FILE LOOADED");
updatePage('short_term')
function clearSelected() {
    $('.resultTable').empty()
    document.querySelectorAll('.time_range').forEach(bt => bt.classList.remove('selected'));
};

function updatePage(time_range) {
    let obj = {
        'time_range': time_range
    }
    console.log(obj)
    $.get($SCRIPT_ROOT + '/api/dateRange/tracks', obj,
        function (data, status, jqXHR) {
            for (let x = 0; x < data['items'].length; x++) {
                console.log(status)
                console.log(data['items'][x])
                let nametopTracks = document.createElement('div');
                let imagetopTracks = document.createElement('td');
                let albImg = document.createElement('img');
                let albumName = document.createElement('span');
                let artistName = document.createElement('span');
                albImg.src = data['items'][x]['album']['images'][0]['url'];
                nametopTracks.append(data['items'][x]['name']);
                imagetopTracks.append(albImg);

                albumName.append(data['items'][x]['album']['name']);
                artistName.append(data['items'][x]['artists'][0]['name']);
                albImg.classList.add('imgTrack');
                nametopTracks.classList.add('nameTrack');
                albumName.classList.add('albumTrack');
                artistName.classList.add('artistTrack');

                // imagetopTracks.append(nametopTracks, albumName, artistName)


                let tableRow = document.createElement('div');
                tableRow.classList.add('result');
                tableRow.append(albImg, nametopTracks, albumName, artistName);
                $('.resultTable').append(tableRow);
            }
        })
};
let shorts = document.querySelector('.short_term');
let medium = document.querySelector('.medium_term');
let long = document.querySelector('.long_term');
document.querySelector('.short_term').addEventListener('click', (e) => {
    e.preventDefault();
    updatePage('short_term');
    clearSelected();
    shorts.classList.add('selected')
});
document.querySelector('.medium_term').addEventListener('click', (e) => {
    e.preventDefault();
    updatePage('medium_term');
    clearSelected();
    medium.classList.add('selected')
});
document.querySelector('.long_term').addEventListener('click', (e) => {
    e.preventDefault();
    updatePage('long_term');
    clearSelected();
    long.classList.add('selected')
});

document.querySelector('.playlist').addEventListener('click', (e) => {
    e.preventDefault();

});

$(".playlist").click(function () {
    $(".selected").val
    $.post($SCRIPT_ROOT + '/api/createPlaylist',
        {
            name: "",
            time_range: $(".selected").val()
        },
        function (data, status) {
            if (status == "success") {
                console.log(status, data)
                alert("Success!");
            }
            else {
                alert("ERROR")
            }
        });
});
updatePage('short_term')