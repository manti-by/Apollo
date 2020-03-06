class WeatherWidget {

    constructor() {
        this.data = {};
        this.status = document.getElementById("status");

        this.target = document.getElementById("weather");
        this.markup = document.getElementById("t-weather").text;
        this.template = Handlebars.compile(this.markup);
    }

    init() {
        this.update();
        setInterval(
            () => this.update(), 5 * 60 * 1000
        );
    }

    render () {
        this.target.innerHTML = this.template(this.data);
    }

    update() {
        getJSON('/api/weather/', (data) => {
            let now = new Date();
            this.status.classList.remove('error');
            this.status.text = 'Last update: ' + now.toLocaleTimeString();

            this.data = {
                temp: data['temp'],
                wind: data['wind_speed'],
                pressure: data['pressure'],
                icon: '/static/img/icons/' + data['icon'] + '.png'
            };
            this.render();
        }, () => {
            this.status.classList.add('error');
            this.status.text = 'Connection error';
        })
    };
}