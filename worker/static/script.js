// Loading base libraries
google.load('jquery', '2.1.4');
google.load('visualization', '1.0', {'packages': ['gauge']});

// Set initial callback
google.setOnLoadCallback(function () {
    var data = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Temp 01', 86],
        ['Temp 02', 79],
        ['Temp 03', 7],
        ['Temp 04', 22],
        ['Temp 05', 28]
    ]);

    var options = {
        width       : 400,
        height      : 120,
        redFrom     : 90,
        redTo       : 100,
        yellowFrom  : 70,
        yellowTo    : 90,
        minorTicks  : 5
    };

    var chart = new google.visualization.Gauge(document.getElementById('charts'));
    chart.draw(data, options);

    setInterval(function() {
        $.get('/data', function(response) {
            if (response['status'] == 200) {
                data.setValue(0, 1, response['result']['term_01']);
                data.setValue(1, 1, response['result']['term_02']);
                data.setValue(2, 1, response['result']['term_03']);
                data.setValue(3, 1, response['result']['term_04']);
                data.setValue(4, 1, response['result']['term_05']);
                chart.draw(data, options);
            } else {
                alert('Something goes wrong!!!')
            }
        });
    }, 60000);
});