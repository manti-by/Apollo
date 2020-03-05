(($) => {

    'use strict';

    class CurrencyWidget {

        constructor() {
            this.template = Handlebars.compile(
                $('#t-currency').html()
            );
            this.canvas = $('#currency');
        }

        init() {
            this.update();
            setInterval(
                () => this.update(), 60 * 60 * 1000
            );
        }

        update() {
            $.getJSON('/api/currency/', (data) => {
                this.canvas.html(
                    this.template({
                        usd_sell: data['usd_sell'],
                        usd_buy: data['usd_buy'],
                        rur_sell: data['rur_sell'],
                        rur_buy: data['rur_buy']
                    })
                );
            });
        };
    }

    $.currency = new CurrencyWidget();

})(jQuery);