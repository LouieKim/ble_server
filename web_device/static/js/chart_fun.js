var toggleBtn_saver = document.querySelector('#toggleBtn_saver');
var interval_timer = 10000;

$(document).ready(function() { 
    get_process();
    get_resource();
    get_today();
    get_timenow();
    screensaver();
});

//===============================================================================

function screensaver(){
    $.ajax({
    type: 'GET',
    contentTypes: 'javascript/json; charset=utf-8',
    data: {},
    dataType: 'json',
    url: 'http://localhost:7070/xscreensaver',
    success: function (e) {

        if (e.xscreensaver_status == "on") {
            toggleBtn_saver.checked = true;
        }
        else if (e.xscreensaver_status == "off") {
            toggleBtn_saver.checked = false;
        }
    }
    })
}

function get_process() {
    $.ajax({
        url: 'http://localhost:7070/process',
        type: 'GET',
        contentType: 'javascript/json; charset=utf-8',
        data: {},
        dataType: 'json',
        success: function (data) {
            document.querySelector('#web_process').innerHTML = data['ninewatt_web'];
        }
    });
}

function get_resource() {
    $.ajax({
        url: 'http://localhost:7070/resource',
        type: 'GET',
        contentType: 'javascript/json; charset=utf-8',
        data: {},
        dataType: 'json',
        success: function (data) {
            document.querySelector('#cpu_usage').innerHTML = data['cpu'];
            document.querySelector('#mem_usage').innerHTML = data['mem'];
            document.querySelector('#hdd_usage').innerHTML = data['hdd'];
        }
    });
}

function get_today() {
    var history_data = null;
    var html = '';
    $.ajax({
        url: 'http://localhost:7070/history/raw/today',
        type: 'GET',
        contentType: 'javascript/json; charset=utf-8',
        data: {},
        dataType: 'json',
        success: function (data) {
            history_data = data.raw_history
            for (var i in history_data) {
                html += '<tr style="margin-left:20px">';
                html += '<td style="width:245px">' + history_data[i][0] + '</td>';
                html += '<td style="width:245px">' + history_data[i][1] + '</td>';
                html += '</tr>';
            }

            $("#dynamicTbody").empty();
            $("#dynamicTbody").append(html);
        }
    });
}

function get_timenow() {
    $.ajax({
        url: 'http://localhost:7070/timenow',
        type: 'GET',
        contentType: 'javascript/json; charset=utf-8',
        data: {},
        dataType: 'json',
        success: function (data) {
            document.querySelector('#timenow').innerHTML = data['time'];
        }
    });
}

//=================================================================