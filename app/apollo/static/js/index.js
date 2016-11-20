(function($){

    'use strict';

    var console = $('.console');
    var console_info = function(message) {
        var date = new Date(Date.now()),
            minutes = date.getMinutes();
        minutes = minutes > 9 ? minutes : '0' + minutes;
        console.append('<div class="info">' + date.getHours() + ':' + minutes + ' ' + message + '</div>');
    };
    var console_error = function(message) {
        var date = new Date(Date.now()),
            minutes = date.getMinutes();
        minutes = minutes > 9 ? minutes : '0' + minutes;
        console.append('<div class="error">' + date.getHours() + ':' + minutes + ' ' + message + '</div>');
    };

    google.charts.load('current', { 'packages': ['gauge'] });

    google.charts.setOnLoadCallback(function () {
        var data_01 = google.visualization.arrayToDataTable([['Label', 'Value'], ['Temp 01', 0]]),
            chart_01 = new google.visualization.Gauge(document.getElementById('chart_01')),
            data_02 = google.visualization.arrayToDataTable([['Label', 'Value'], ['Temp 02', 0]]),
            chart_02 = new google.visualization.Gauge(document.getElementById('chart_02')),
            data_03 = google.visualization.arrayToDataTable([['Label', 'Value'], ['Temp 03', 0]]),
            chart_03 = new google.visualization.Gauge(document.getElementById('chart_03')),
            data_04 = google.visualization.arrayToDataTable([['Label', 'Value'], ['Temp 04', 0]]),
            chart_04 = new google.visualization.Gauge(document.getElementById('chart_04')),
            data_05 = google.visualization.arrayToDataTable([['Label', 'Value'], ['Temp 05', 0]]),
            chart_05 = new google.visualization.Gauge(document.getElementById('chart_05'));

        var spirit_temp_options = {
                width       : 170,
                height      : 170,
                redFrom     : 85,
                redTo       : 100,
                yellowFrom  : 81,
                yellowTo    : 85,
                minorTicks  : 5
            },
            water_temp_options = {
                width       : 110,
                height      : 110,
                redFrom     : 40,
                redTo       : 100,
                yellowFrom  : 25,
                yellowTo    : 40,
                minorTicks  : 5
            };

        chart_01.draw(data_01, spirit_temp_options);
        chart_02.draw(data_02, spirit_temp_options);
        chart_03.draw(data_03, water_temp_options);
        chart_04.draw(data_04, water_temp_options);
        chart_05.draw(data_05, water_temp_options);

        console_info('Charts inited');

        var prev = {term_01: 0, term_02: 0, term_03: 0, term_04: 0, term_05: 0},
            message = [];
        setInterval(function() {
            $.get('/api?latest=1', function(response) {
                if (response['status'] == 200) {
                    data_01.setValue(0, 1, response['data']['term_01']);
                    chart_01.draw(data_01, spirit_temp_options);
                    data_02.setValue(0, 1, response['data']['term_02']);
                    chart_02.draw(data_02, spirit_temp_options);

                    data_03.setValue(0, 1, response['data']['term_03']);
                    chart_03.draw(data_03, water_temp_options);
                    data_04.setValue(0, 1, response['data']['term_04']);
                    chart_04.draw(data_04, water_temp_options);
                    data_05.setValue(0, 1, response['data']['term_05']);
                    chart_05.draw(data_05, water_temp_options);

                    if (prev['term_01'] && prev['term_01'] != response['data']['term_01'])
                        message.push(1);
                    if (prev['term_02'] && prev['term_02'] != response['data']['term_02'])
                        message.push(2);
                    if (prev['term_03'] && prev['term_03'] != response['data']['term_03'])
                        message.push(3);
                    if (prev['term_04'] && prev['term_04'] != response['data']['term_04'])
                        message.push(4);
                    if (prev['term_05'] && prev['term_05'] != response['data']['term_05'])
                        message.push(5);

                    if (message.length) {
                        console_info('Sensors ' + message.join(', ') + ' changed;');
                        console.scrollTop(200);
                    }

                    prev = response['data'];
                    message = [];
                } else {
                    console_error(response['message']);
                }
            });
        }, 5000);
    });
})(jQuery);
