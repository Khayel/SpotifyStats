console.log("THIS FILE LOOADED");
$(document).on('click', '#submit', function (e) {
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
            console.log(data)
        })


})