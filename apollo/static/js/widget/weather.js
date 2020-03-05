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
            $.getJSON(
                'https://api.openweathermap.org/data/2.5/weather?q=Minsk,by&units=metric&appid=aec9289a4fe49b1bca7296d08c1e170b',
                (data) => {
                    this.canvas.html(
                        this.template({
                            temp: data['main']['temp'],
                            wind: data['wind']['speed'],
                            pressure: data['main']['pressure'],
                            icon: 'http://openweathermap.org/img/w/' + data['weather'][0]['icon'] + '.png'
                        })
                    );

                    $('.wind-direction i').css('transform', 'rotate(' + (data['wind']['deg'] - 90) + 'deg)');
                }
            )
        };
    }

    $.weather = new WeatherWidget();

})(jQuery);