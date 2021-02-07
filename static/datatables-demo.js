// Call the dataTables jQuery plugin
document.addEventListener("DOMContentLoaded", function (event) {
  //do work

  for (let x = 0; x < topTracks['items'].length; x++) {
    console.log(x)
    console.log(topTracks['items'][x])
    let nametopTracks = document.createElement('td');
    let imagetopTracks = document.createElement('td');
    let albImg = document.createElement('img');
    let albumName = document.createElement('td');
    let artistName = document.createElement('td');
    albImg.src = topTracks['items'][x]['album']['images'][2]['url'];
    nametopTracks.append(topTracks['items'][x]['name']);
    imagetopTracks.append(albImg);

    albumName.append(topTracks['items'][x]['album']['name']);
    artistName.append(topTracks['items'][x]['artists'][0]['name']);


    let tableRow = document.createElement('tr');
    tableRow.append(imagetopTracks, nametopTracks, albumName, artistName);
    document.querySelector('.topTrackResult').append(tableRow)
  }
});

$(document).ready(function () {
  $('#dataTable').DataTable();
});
