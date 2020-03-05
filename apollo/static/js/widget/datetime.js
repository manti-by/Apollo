(($) => {

    'use strict';

    class DatetimeWidget {

        constructor() {
            this.template = Handlebars.compile(
                $('#t-datetime').html()
            );
            this.canvas = $('#datetime');
        }

        init() {
            this.update();
            setInterval(
                () => this.update(), 1000
            );
        }

        update() {
            let datetime = new Date();

            this.canvas.html(
                this.template({
                    date: datetime.toLocaleDateString(),
                    time: datetime.toLocaleTimeString()
                })
            );
        };
    }

    $.datetime = new DatetimeWidget();

})(jQuery);