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
        }

        update() {
            $.get(
                'https://www.mtbank.by/currxml.php?ver=2',
                (response) => {
                    let usd_sell = 0, usd_buy = 0,
                        rur_sell = 0, rur_buy = 0;

                    $.each(response.all.item('0').children, (x, element) => {
                        if (element.id === '168,768,968,868') {
                            $.each(element.children, (y, currency) => {
                                if (currency.children[0].textContent === 'BYN' &&
                                    currency.children[1].textContent === 'USD') {
                                    usd_buy = currency.children[2].textContent ;
                                    usd_sell = currency.children[3].textContent ;
                                }
                                if (currency.children[0].textContent === 'BYN' &&
                                    currency.children[1].textContent === 'RUB') {
                                    rur_buy = currency.children[2].textContent * 10;
                                    rur_sell = currency.children[3].textContent * 10;
                                }
                            });
                        }
                    });

                    this.canvas.html(
                        this.template({
                            usd_sell: usd_sell,
                            usd_buy: usd_buy,
                            rur_sell: rur_sell,
                            rur_buy: rur_buy,
                        })
                    );
                }
            )
        };
    }

    $.currency = new CurrencyWidget();

})(jQuery);