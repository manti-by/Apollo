(($) => {

    'use strict';

    class PlantsLatestWidget {
        constructor() {
            this.status = $('#status');
            this.temp = $('#plants-latest-temp').get(0);
            this.humidity = $('#plants-latest-humidity').get(0);
            this.moisture = $('#plants-latest-moisture').get(0);
            this.luminosity = $('#plants-latest-luminosity').get(0);

            let window_width = $(window).width(),
                length;

            if (window_width > 1000) {
                length = 200;
            } else if (window_width > 425) {
                length = 250;
            } else {
                length = 300;
            }

            $('.plants-latest canvas')
                .attr('width', length)
                .attr('height', length);
        }

        init() {
            this.temp_chart = new Sensor(this.temp, {
                color: 'rgba(119, 201, 197, 1)',
                fgcolor: 'rgba(119, 201, 197, .2)',
                unit: '°C'
            });
            this.humidity_chart = new Sensor(this.humidity, {
                color: 'rgba(63, 112, 181, 1)',
                fgcolor: 'rgba(63, 112, 181, .2)',
                unit: '%'
            });
            this.moisture_chart = new Sensor(this.moisture, {
                color: 'rgba(120, 54, 152, 1)',
                fgcolor: 'rgba(120, 54, 152, .2)',
                unit: '%'
            });
            this.luminosity_chart = new Sensor(this.luminosity, {
                color: 'rgba(152, 205, 239, 1)',
                fgcolor: 'rgba(152, 205, 239, .2)',
                unit: '%'
            });

            this.update();
            setInterval(
                () => this.update(),
                5 * 60 * 1000
            );
        }

        update() {
            $.getJSON('/api?limit=1', (data) => {
                this.temp_chart.draw(data['temp'][0]);
                this.humidity_chart.draw(data['humidity'][0]);
                this.moisture_chart.draw(data['moisture'][0]);
                this.luminosity_chart.draw(data['luminosity'][0]);
            }).done(() => {
                let now = new Date();

                this.status
                    .removeClass('text-danger')
                    .addClass('text-secondary')
                    .text(
                        'Last update: ' + now.toLocaleTimeString()
                    );
            }).fail(() => {
                this.status
                    .removeClass('text-secondary')
                    .addClass('text-danger')
                    .text('Connection error');
            });
        }

    }

    $.indoor_climate = new PlantsLatestWidget();

})(jQuery);