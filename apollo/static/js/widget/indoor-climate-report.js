class IndoorClimateReportWidget {
    constructor() {
        this.data = {};
        this.status = document.getElementById("status");

        this.target = document.getElementById("indoor-climate-report");
        this.markup = document.getElementById("t-indoor-climate-report").text;
        this.template = Handlebars.compile(this.markup);

        this.options = {
            responsive: true,
            aspectRatio:  window.innerWidth <= 425 ? 1 : 2,
            legend: {
                position: 'bottom',
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Date'
                    }
                }],
                yAxes: [{
                    name: 'A',
                    position: 'left',
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Temperature'
                    }
                }, {
                    name: 'B',
                    position: 'right',
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Humidity / Moisture / Luminosity'
                    }
                }]
            }
        };
    }

    init() {
        this.render();

        this.update();
        setInterval(
            () => this.update(),
            5 * 60 * 1000
        );
    }

    render() {
        this.target.innerHTML = this.template(this.data);

        this.canvas = document.getElementById("indoor-climate-report-canvas");
        this.chart = new Chart(this.canvas, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    index: 'temp',
                    label: 'Temperature, C',
                    fill: false,
                    borderColor: 'rgb(119, 201, 197)',
                    backgroundColor: 'rgb(119, 201, 197)',
                    data: [],
                    yAxesGroup: 'A'
                }, {
                    index: 'humidity',
                    label: 'Humidity, %',
                    fill: false,
                    borderColor: 'rgba(63, 112, 181)',
                    backgroundColor: 'rgba(63, 112, 181)',
                    data: [],
                    yAxesGroup: 'B'
                }, {
                    index: 'moisture',
                    label: 'Moisture, %',
                    fill: false,
                    borderColor: 'rgb(120, 54, 152)',
                    backgroundColor: 'rgb(120, 54, 152)',
                    data: [],
                    yAxesGroup: 'B'
                }, {
                    index: 'luminosity',
                    label: 'Luminosity, %',
                    fill: false,
                    borderColor: 'rgb(152, 205, 239)',
                    backgroundColor: 'rgb(152, 205, 239)',
                    data: [],
                    yAxesGroup: 'B'
                }]
            },
            options: this.options,
        });

        document.querySelector("#limit, #group").onchange = () => this.update();
    }

    update() {
        let limit = document.getElementById("limit").value,
            group = document.getElementById("group").value;

        getJSON('/api/sensors/?limit=' + limit + '&group=' + group, (data) => {
            let now = new Date();
            this.status.classList.remove('error');
            this.status.text = 'Last update: ' + now.toLocaleTimeString();

            this.chart.data.labels = data['label'];

            this.chart.data.datasets.forEach((dataset) => {
                dataset.data = data[dataset.index];
            });

            this.chart.options.scales.yAxes.forEach((value) => {
                value.ticks = {
                    min: 0,
                    max: 100,
                    stepSize: 10
                };
            });

            this.chart.update();
        }, () => {
            this.status.classList.add('error');
            this.status.text = 'Connection error';
        });
    }
}