// Call the dataTables jQuery plugin
//do work
/*
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
*/
console.log("THIS FILE LOOADED");
$(document).on('click', '.time_range', function (e) {
  $('.topTrackResult').empty()

  var obj = {
    'time_range': $('.time_range:checked').val()
  }
  console.log(obj)

  $.get($SCRIPT_ROOT + '/api/dateRange', obj,
    function (data, status, jqXHR) {
      for (let x = 0; x < data['items'].length; x++) {
        console.log(status)
        console.log(data['items'][x])
        let nametopTracks = document.createElement('td');
        let imagetopTracks = document.createElement('td');
        let albImg = document.createElement('img');
        let albumName = document.createElement('td');
        let artistName = document.createElement('td');
        albImg.src = data['items'][x]['album']['images'][2]['url'];
        nametopTracks.append(data['items'][x]['name']);
        imagetopTracks.append(albImg);

        albumName.append(data['items'][x]['album']['name']);
        artistName.append(data['items'][x]['artists'][0]['name']);


        let tableRow = document.createElement('tr');
        tableRow.append(imagetopTracks, nametopTracks, albumName, artistName);
        $('.topTrackResult').append(tableRow);
      }
    })
});
document.querySelector('#defaultLength').click();