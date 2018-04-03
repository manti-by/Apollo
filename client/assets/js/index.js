(function($){

    'use strict';

    $.app = {
        raw_data: null,
        crt_data: null,

        colors: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)'
        ],

        console: $('#console'),

        print: function(message, level) {
            var date = new Date(Date.now()),
                minutes = date.getMinutes();

            minutes = minutes > 9 ? minutes : '0' + minutes;
            this.console.append(
                '<div class="' + level + '">' + date.getHours() + ':' + minutes + ' ' + message + '</div>'
            );
        },

        info: function(message) {
            this.print(message, 'info');
        },

        error: function(message) {
            this.print(message, 'error');
        },

        update: function() {
            var view = this;

            $.ajax({
                url: 'http://127.0.0.1:5000',
                method: 'GET',
                dataType: 'json',
                contentType: 'application/json',
                crossDomain: true,
                success: function(response) {
                    if (response['status'] === 200) {
                        view.raw_data = response['data'];
                        view.info('Data updated');

                        view.compile();
                        view.draw();
                    } else {
                        view.error(response['message']);
                    }
                },
                error: function () {
                    view.error('Can\'t load data from server');
                }
            });
        },

        compile: function() {
            if (!this.raw_data) return;

            this.crt_data = {
                labels: [],
                datasets: []
            };

            var view = this,
                color = 0,
                datasets, labels, datetime;

            $.each(this.raw_data, function (sensor, data) {
                labels = [];
                datasets = [];

                for (var i = 0; i < data.length; i++) {
                    datetime = new Date(Date.parse(data[i]['datetime']));
                    labels.push(datetime.toLocaleTimeString());
                    datasets.push(data[i]['temp']);
                }

                view.crt_data['labels'] = labels;
                view.crt_data['datasets'].push({
                    label: sensor,
                    data: datasets,
                    borderColor: view.colors[color],
                    borderWidth: 2,
                    fill: false
                });

                color++;
            });
        },

        draw: function() {
            this.compile();

            if (!this.crt_data) return;

            Chart.scaleService.updateScaleDefaults('linear', {
                ticks: {
                     min: 15,
                     max: 30
                }
            });

            var ctx = document.getElementById('sensors').getContext('2d'),
                crt = new Chart(ctx, {
                    type: 'line',
                    data: this.crt_data
                });
        }
    };

    $.app.info('Application started');
    $.app.update();

    setInterval(function() {
        $.app.update();
    }, 60000);
})(jQuery);