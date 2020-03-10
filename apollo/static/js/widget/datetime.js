class DatetimeWidget {

  constructor() {
    this.data = {};
    this.target = document.getElementById("datetime");
    this.markup = document.getElementById("t-datetime").text;
    this.template = Handlebars.compile(this.markup);
  }

  init() {
    this.update();
    setInterval(
      () => this.update(), 10 * 1000
    );
  }

  render() {
    this.target.innerHTML = this.template(this.data);
  }

  update() {
    let datetime = new Date(),
      day = datetime.getDate(),
      month = datetime.getMonth() + 1,
      hours = datetime.getHours(),
      minutes = datetime.getMinutes();

    day = day < 10 ? '0' + day : day;
    month = month < 10 ? '0' + month : month;
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;

    this.data = {
      date: day + '-' + month + '-' + datetime.getFullYear(),
      time: hours + '<span class="separator">:</span>' + minutes,
    };
    this.render();
  };
}