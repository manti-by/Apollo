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

    google.charts.load('current', { 'packages': ['corechart', 'gauge'] });

    google.charts.setOnLoadCallback(function () {
        // Draw charts
        var data_01 = google.visualization.arrayToDataTable([['Label', 'Value'], ['Tank Temp', 0]]),
            chart_01 = new google.visualization.Gauge(document.getElementById('chart_01')),
            data_02 = google.visualization.arrayToDataTable([['Label', 'Value'], ['Column Temp', 0]]),
            chart_02 = new google.visualization.Gauge(document.getElementById('chart_02')),
            data_03 = google.visualization.arrayToDataTable([['Label', 'Value'], ['Spirit Temp', 0]]),
            chart_03 = new google.visualization.Gauge(document.getElementById('chart_03'));

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
                width       : 170,
                height      : 170,
                redFrom     : 40,
                redTo       : 100,
                yellowFrom  : 25,
                yellowTo    : 40,
                minorTicks  : 5
            };

        chart_01.draw(data_01, spirit_temp_options);
        chart_02.draw(data_02, spirit_temp_options);
        chart_03.draw(data_03, water_temp_options);

        console_info('Charts inited');

        // Draw graph
        var graph = new google.charts.Line(document.getElementById('graph')),
            graph_data = new google.visualization.DataTable(),
            graph_options = {
                chart: {
                    title: 'Sensors data',
                    subtitle: 'updates every minute'
                },
                width: $(window).width() - 20,
                height: 500
            },
            shot = 0;

        graph_data.addColumn('number', 'Shot');
        graph_data.addColumn('number', 'Tank Temp');
        graph_data.addColumn('number', 'Column Temp');
        graph_data.addColumn('number', 'Spirit Temp');

        $.get('/api', function(response) {
            if (response['status'] == 200) {
                for (shot = 0; shot < response['data'].length; shot++) {
                    graph_data.addRow([
                        shot,
                        response['data'][shot]['term_01'],
                        response['data'][shot]['term_02'],
                        response['data'][shot]['term_03']
                    ]);
                }
                graph.draw(graph_data, graph_options);
                console_info('Graph inited');
            } else {
                console_error(response['message']);
            }
        });

        // Update data
        var prev = {term_01: 0, term_02: 0, term_03: 0},
            message = [], data = [];

        setInterval(function() {
            $.get('/api?latest=1', function(response) {
                if (response['status'] == 200) {
                    // Update charts
                    data_01.setValue(0, 1, response['data']['term_01']);
                    chart_01.draw(data_01, spirit_temp_options);
                    data_02.setValue(0, 1, response['data']['term_02']);
                    chart_02.draw(data_02, spirit_temp_options);
                    data_03.setValue(0, 1, response['data']['term_03']);
                    chart_03.draw(data_03, water_temp_options);

                    // Update graph
                    graph_data.addRow([
                        shot,
                        response['data']['term_01'],
                        response['data']['term_02'],
                        response['data']['term_03']
                    ]);
                    graph.draw(graph_data, graph_options);

                    // Check changes
                    if (prev['term_01'] && prev['term_01'] != response['data']['term_01'])
                        message.push(1);
                    if (prev['term_02'] && prev['term_02'] != response['data']['term_02'])
                        message.push(2);
                    if (prev['term_03'] && prev['term_03'] != response['data']['term_03'])
                        message.push(3);

                    // Print console message
                    if (message.length) {
                        console_info('Sensors ' + message.join(', ') + ' changed;');
                        console.scrollTop(200);
                    }

                    shot++;
                    prev = response['data'];
                    data.push(response['data']);
                    message = [];
                } else {
                    console_error(response['message']);
                }
            });
        }, 5000);
    });
})(jQuery);
