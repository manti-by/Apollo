(($) => {

    'use strict';

    class PlantsReportWidget {
        constructor() {
            this.status = $('#status');
            this.chart = $('#plants-report');
            this.is_mobile = $(window).width() <= 425;

            this.options = {
                responsive: true,
                aspectRatio: this.is_mobile ? 1 : 2,
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

            this.scales = {
                A: {
                    absolute: {
                        min: 0,
                        max: 100
                    },
                    relative: {
                        min: 5,
                        max: 70
                    }
                },
                B: {
                    absolute: {
                        min: 0,
                        max: 100
                    },
                    relative: {
                        min: 5,
                        max: 70
                    }
                }
            };
        }

        init() {
            this.chart = new Chart(this.chart, {
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

            this.update();

            setInterval(
                () => this.update(),
                5 * 60 * 1000
            );

            $('#limit, #group, .type').on(
                'change',
                () => this.update()
            );
        }

        update() {
            let limit = $('#limit').val(),
                group = $('#group').val(),
                type = $('.type:checked').val();

            $.getJSON('/api?limit=' + limit + '&group=' + group, (data) => {
                this.chart.data.labels = data['label'];

                this.chart.data.datasets.forEach((dataset) => {
                    dataset.data = data[dataset.index];
                });

                this.chart.options.scales.yAxes.forEach((value) => {
                    value.ticks = {
                        min: this.scales[value.name][type]['min'],
                        max: this.scales[value.name][type]['max'],
                        stepSize: 10
                    };
                });

                this.chart.update();
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

    $.indoor_climate_report = new PlantsReportWidget();

})(jQuery);