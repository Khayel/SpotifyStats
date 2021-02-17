function clearSelected() {
    $('.topArtists').empty()
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
                let nametopArtist = document.createElement('td');
                let imagetopArtist = document.createElement('td');
                let albImg = document.createElement('img');

                let spLink = document.createElement('a');
                spLink.href = item['external_urls']['spotify'];
                albImg.src = item['images'][0]['url'];
                spLink.append(item['name']);
                imagetopArtist.append(albImg, spLink);
                albImg.classList.add('imgArtist');
                let tableRow = document.createElement('tr');
                tableRow.append(imagetopArtist);
                $('.topArtists').append(tableRow);

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
