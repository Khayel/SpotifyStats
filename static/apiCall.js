console.log("THIS FILE LOOADED");
$(document).on('click', '#submit', function (e) {
    $('.listResult').empty()
    e.preventDefault()
    var obj = {};

    $('#param').val();
    obj = {
        'apiUrl': $('#apiUrl').val(),
        'param': $('#param').val()
    }
    console.log(obj)

    $.get($SCRIPT_ROOT + '/api', obj,
        function (data, status, jqXHR) {
            $('#apiResult').append(data);
            let resultObj = data.items;
            console.log(data['items'])
            for (let x = 0; x <= data['items'].length; x++) {
                console.log(data['items'][x])
                let nameData = document.createElement('td');
                let imageData = document.createElement('td');
                let albImg = document.createElement('img');
                albImg.src = data['items'][x]['album']['images'][2]['url'];
                nameData.append(data['items'][x]['name']);
                imageData.append(albImg)

                let tableRow = document.createElement('tr');
                tableRow.append(imageData, nameData);
                $('.listResult').append(tableRow);
            }



        })


})