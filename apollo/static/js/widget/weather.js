(($) => {

    'use strict';

    class WeatherWidget {

        constructor() {
            this.template = Handlebars.compile(
                $('#t-weather').html()
            );
            this.canvas = $('#weather');
        }

        init() {
            this.update();
            setInterval(
                () => this.update(), 5 * 60 * 1000
            );
        }

        update() {
            $.getJSON('/api/weather/', (data) => {
                this.canvas.html(
                    this.template({
                        temp: data['temp'],
                        wind: data['wind_speed'],
                        pressure: data['pressure'],
                        icon: 'http://openweathermap.org/img/w/' + data['icon'] + '.png'
                    })
                );
                $('.wind-direction i').css('transform', 'rotate(' + (data['wind_direction'] - 90) + 'deg)');
            })
        };
    }

    $.weather = new WeatherWidget();

})(jQuery);