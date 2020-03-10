class CurrencyWidget {

  constructor() {
    this.data = {};
    this.fields = ['usd_buy', 'usd_sell', 'eur_buy', 'eur_sell', 'rur_buy', 'rur_sell'];
    this.status = document.getElementById("status");

    this.target = document.getElementById("currency");
    this.markup = document.getElementById("t-currency").text;
    this.template = Handlebars.compile(this.markup);
  }

  init() {
    this.update();
    setInterval(
      () => this.update(), 60 * 60 * 1000
    );
  }

  render() {
    for (let index in this.fields)
      this.data[this.fields[index]] =
        this.data[this.fields[index]] ? this.data[this.fields[index]].toFixed(2) : 0;

    this.target.innerHTML = this.template(this.data);
  }

  update() {
    getJSON('/api/currency/', (data) => {
      let now = new Date();
      this.status.classList.remove('error');
      this.status.text = 'Last update: ' + now.toLocaleTimeString();

      this.data = data;
      this.render();
    }, () => {
      this.status.classList.add('error');
      this.status.text = 'Connection error';
    });
  };
}