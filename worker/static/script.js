// Loading base libraries
google.load('jquery', '1.7.1');
google.load('visualization', '1.0', {'packages': ['gauge']});

// Set initial callback
google.setOnLoadCallback(function () {
    // Default options
    var options = {
            width       : 400,
            height      : 120,
            redFrom     : 40,
            redTo       : 100,
            yellowFrom  : 25,
            yellowTo    : 40,
            minorTicks  : 5
        };

    // Temp 01
    var data_01 = google.visualization.arrayToDataTable([['Label', 'Value'],['Temp 01', 86]]),
        chart_01 = new google.visualization.Gauge(document.getElementById('chart_01')),
        options_01 = options;

    options_01.redFrom = 96;
    options_01.yellowFrom = 90;
    options_01.yellowTo = 96;
    chart_01.draw(data_01, options_01);

    // Temp 02
    var data_02 = google.visualization.arrayToDataTable([['Label', 'Value'],['Temp 02', 79]]),
        chart_02 = new google.visualization.Gauge(document.getElementById('chart_02')),
        options_02 = options;

    options_01.redFrom = 90;
    options_01.yellowFrom = 86;
    options_01.yellowTo = 90;
    chart_02.draw(data_02, options_01);

    // Temp 03
    var data_03 = google.visualization.arrayToDataTable([['Label', 'Value'],['Temp 03', 7]]),
        chart_03 = new google.visualization.Gauge(document.getElementById('chart_03')),
        options_03 = options;

    options_03.redFrom = 30;
    options_03.yellowFrom = 20;
    options_03.yellowTo = 30;
    chart_03.draw(data_03, options_03);

    // Temp 04
    var data_04 = google.visualization.arrayToDataTable([['Label', 'Value'],['Temp 04', 21]]),
        chart_04 = new google.visualization.Gauge(document.getElementById('chart_04')),
        data_05 = google.visualization.arrayToDataTable([['Label', 'Value'],['Temp 05', 26]]),
        chart_05 = new google.visualization.Gauge(document.getElementById('chart_05'));

    chart_04.draw(data_04, options);
    chart_05.draw(data_05, options);

    setInterval(function() {
        $.get('/data', function(response) {
            if (response['status'] == 200) {
                data_01.setValue(0, 1, response['result']['term_01']);
                chart_01.draw(data, options_01);

                data_02.setValue(0, 1, response['result']['term_02']);
                chart_02.draw(data, options_02);

                data_03.setValue(0, 1, response['result']['term_03']);
                chart_03.draw(data, options_03);

                data_04.setValue(0, 1, response['result']['term_04']);
                chart_04.draw(data, options);

                data_05.setValue(0, 1, response['result']['term_05']);
                chart_05.draw(data, options);
            } else {
                alert('Something goes wrong!!!')
            }
        });
    }, 60000);
});