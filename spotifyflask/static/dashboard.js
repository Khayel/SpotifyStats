

for (let x = 0; x < top3Artist['items'].length; x++) {
    console.log(x)
    console.log(top3Artist['items'][x])
    let nametop3Artist = document.createElement('td');
    let imagetop3Artist = document.createElement('td');
    let albImg = document.createElement('img');
    albImg.src = top3Artist['items'][x]['images'][2]['url'];
    nametop3Artist.append(top3Artist['items'][x]['name']);
    imagetop3Artist.append(albImg);

    let tableRow = document.createElement('tr');
    tableRow.append(imagetop3Artist, nametop3Artist);
    document.querySelector('.topArtistResult').append(tableRow)
}


for (let x = 0; x < top3Track['items'].length; x++) {
    console.log(x)
    console.log(top3Track['items'][x])
    let nametop3Track = document.createElement('td');
    let imagetop3Track = document.createElement('td');
    let albImg = document.createElement('img');
    albImg.src = top3Track['items'][x]['album']['images'][2]['url'];
    nametop3Track.append(top3Track['items'][x]['name']);
    imagetop3Track.append(albImg)

    let tableRow = document.createElement('tr');
    tableRow.append(imagetop3Track, nametop3Track);
    document.querySelector('.topTrackResult').append(tableRow)
}

