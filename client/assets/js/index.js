(function($){

    'use strict';

    $.app = {
        data: [
            ['Guest Room', [23, 24, 23, 22, 21]],
            ['Bath Room', [26, 27, 28, 28, 28]],
            ['Sleeping Room', [19, 19, 20, 21, 21]],
            ['Working Room', [22, 22, 23, 22, 22]],
            ['Reception', [17, 19, 21, 17, 18]]
        ],

        datasets: [],

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

            $.get('/', function(response) {
                if (response['status'] === 200) {
                    view.data = response['data'];
                    view.info('Data updated');

                    view.compile();
                    view.draw();
                } else {
                    view.error(response['message']);
                }
            }).fail(function() {
                view.error('Can\'t load data from server');
            });
        },

        compile: function() {
            this.datasets = [];

            for (var i = 0; i < this.data.length; i++) {
                this.datasets.push({
                    label: this.data[i][0],
                    data: this.data[i][1],
                    borderColor: this.colors[i],
                    borderWidth: 2,
                    fill: false
                });
            }
        },

        draw: function() {
            this.compile();

            Chart.scaleService.updateScaleDefaults('linear', {
                ticks: {
                     min: 15,
                     max: 30
                }
            });

            var ctx = document.getElementById('sensors').getContext('2d'),
                crt = new Chart(ctx, {
                    type: 'line',
                    data: {
                      labels: ["18:00", "18:05", "18:10", "18:15", "18:20"],
                      datasets: this.datasets
                    }
                });
        }
    };

    $.app.info('Application started');
    $.app.update();
    $.app.draw();

    setInterval(function() {
        $.app.update();
    }, 60000);
})(jQuery);