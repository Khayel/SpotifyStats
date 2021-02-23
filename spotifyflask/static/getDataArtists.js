function clearSelected() {
    $('.resultTable').empty()
    document.querySelectorAll('.time_range').forEach(bt => bt.classList.remove('selected'));
};

function updatePage(time_range) {
    let obj = {
        'time_range': time_range
    }
    $.get($SCRIPT_ROOT + '/api/dateRange/artists', obj,
        function (data, status, jqXHR) {
            console.log(data)
            data['items'].forEach((item) => {
                let nametopArtist = document.createElement('div');
                let imagetopArtist = document.createElement('td');
                let albImg = document.createElement('img');

                let spLink = document.createElement('a');
                spLink.href = item['external_urls']['spotify'];
                albImg.src = item['images'][0]['url'];
                nametopArtist.append(item['name'])
                spLink.append(albImg)
                spLink.append(nametopArtist);

                imagetopArtist.append(spLink);
                albImg.classList.add('imgArtist');
                albImg.href = item['external_urls']['spotify'];
                albImg.classList.add('imgTrack');
                let tableRow = document.createElement('div');
                tableRow.classList.add('result');
                tableRow.append(albImg, nametopArtist);
                $('.resultTable').append(tableRow);

            })
        })
}
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

// Default page looad
updatePage('short_term')
