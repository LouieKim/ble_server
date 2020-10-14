var toggleBtn = document.querySelector('#toggle_btn');
var toggleBtn_saver = document.querySelector('#toggle_btn_saver');

var ctx = document.getElementById('myChart').getContext('2d');

var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: '',
            data: [],
            backgroundColor: []
        }]
    },
    options: {
        responsive: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});
//===========================================================

$(document).ready(function() { 
    get_timenow();
    get_process();
    get_resource();
    get_day_history();
    screensaver();
});

function get_day_history() {
    var date_label = []
    var value_data = []
    var backgd = []
    var history_data = null
    $.ajax({
        url: 'http://localhost:7070/get/day',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            history_data = data.day_history

            for (var i in history_data) {
                date_label.push(history_data[i][0].slice(8, 10))
                value_data.push(history_data[i][1])
                backgd.push('rgba(44, 248, 250, 1)')
            }
        }
    }).done(function (res) {
        addData(myChart, date_label, '일간사용량', value_data, backgd);
    });
}

function get_month_history() {
    var date_label = []
    var value_data = []
    var backgd = []
    var history_data = null
    $.ajax({
        url: 'http://localhost:7070/get/month',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            history_data = data.month_history

            for (var i in history_data) {
                date_label.push(history_data[i][0].slice(5, 7))
                value_data.push(history_data[i][1])
                backgd.push('rgba(44, 248, 250, 1)')
            }
        }
    }).done(function (res) {
        addData(myChart, date_label, '월간사용량', value_data, backgd);
    });
}

function addData(chart, label, name, data, backgd) {
    chart.data.labels = label;
    chart.data.datasets[0].label = name
    chart.data.datasets[0].data = data;
    chart.data.datasets[0].backgroundColor = backgd;
    chart.update();
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

function toggle_update_graph() {
    if (toggleBtn.checked) {
        get_month_history()
    } else {
        get_day_history()
    }
}

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

 // toggleBtn.checked = true;
 toggleBtn.addEventListener('change', function () {
    if (toggleBtn.checked) {
        get_month_history()
    } else {
        get_day_history()
    }
});

toggleBtn_saver.addEventListener('change', function () {
    if (toggleBtn_saver.checked) {
        $.ajax({
            type: 'GET',
            contentTypes: 'javascript/json; charset=utf-8',
            data: {},
            dataType: 'json',
            url: 'http://localhost:7070/xscreensaver/on',
            success: function (e) {
            }
        })
    } else {
        $.ajax({
            type: 'GET',
            contentTypes: 'javascript/json; charset=utf-8',
            data: {},
            dataType: 'json',
            url: 'http://localhost:7070/xscreensaver/off',
            success: function (e) {
            }
        })
    }
})