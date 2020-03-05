class IndoorClimateWidget {

    constructor() {
        this.data = {};
        this.status = document.getElementById("status");

        this.target = document.getElementById("indoor-climate");
        this.markup = document.getElementById("t-indoor-climate").text;
        this.template = Handlebars.compile(this.markup);
    }

    init() {
        this.render();

        this.update();
        setInterval(
            () => this.update(),
            5 * 60 * 1000
        );
    }

    render () {
        this.target.innerHTML = this.template(this.data);

        this.temp = document.getElementById("indoor-climate-temp-canvas");
        this.humidity = document.getElementById("indoor-climate-humidity-canvas");
        this.moisture = document.getElementById("indoor-climate-moisture-canvas");
        this.luminosity = document.getElementById("indoor-climate-luminosity-canvas");

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
    }

    update() {
        getJSON('/api/sensors/?limit=1', (data) => {
            let now = new Date();
            this.status.classList.remove('error');
            this.status.text = 'Last update: ' + now.toLocaleTimeString();

            this.temp_chart.draw(data['temp'][0]);
            this.humidity_chart.draw(data['humidity'][0]);
            this.moisture_chart.draw(data['moisture'][0]);
            this.luminosity_chart.draw(data['luminosity'][0]);
        }, () => {
            this.status.classList.add('error');
            this.status.text = 'Connection error';
        });
    }

}