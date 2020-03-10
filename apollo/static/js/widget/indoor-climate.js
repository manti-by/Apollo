class IndoorClimateWidget {

  constructor() {
    this.data = {};
    this.colors = {
      humidity: 'rgba(252, 166, 57, 1)',
      moisture: 'rgba(69, 137, 105, 1)',
      luminosity: 'rgba(40, 63, 158, 1)',
    };

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

  render() {
    this.target.innerHTML = this.template(this.data);

    this.temp = document.querySelector("#indoor-climate .temp .arrow");
    this.humidity = document.querySelector("#indoor-climate .humidity canvas");
    this.moisture = document.querySelector("#indoor-climate .moisture canvas");
    this.luminosity = document.querySelector("#indoor-climate .luminosity canvas");
  }

  renderGauge() {
    let offset = 220 * Math.PI / 180,
      radians = this.data['temp'] / 100 * 260 * Math.PI / 180 - offset;

    this.temp.setAttribute("style", "transform:rotate(" + radians + "deg)");
  }

  renderCharts() {
    this.drawChart(this.humidity, 'humidity');
    this.drawChart(this.moisture, 'moisture');
    this.drawChart(this.luminosity, 'luminosity');
  }

  drawChart(canvas, sensor) {
    let ctx = canvas.getContext('2d'),
      cX = Math.floor(canvas.width / 2),
      cY = Math.floor(canvas.height / 2),
      radius = Math.min(cX, cY) - 3,
      offset = -30,
      radians = this.data[sensor] / 100 * 260 * Math.PI / 180 - offset;

    ctx.strokeStyle = this.colors[sensor];
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.moveTo(cX, cY);
    ctx.beginPath();
    ctx.arc(cX, cY, radius, -offset, radians);
    ctx.stroke();
  }

  update() {
    getJSON('/api/sensors/?limit=1', (data) => {
      let now = new Date();
      this.status.classList.remove('error');
      this.status.text = 'Last update: ' + now.toLocaleTimeString();

      this.data = {
        temp: data['temp'][0],
        humidity: data['humidity'][0],
        moisture: data['moisture'][0],
        luminosity: data['luminosity'][0],
      };
      this.renderGauge();
      this.renderCharts();
    }, () => {
      this.status.classList.add('error');
      this.status.text = 'Connection error';
    });
  }

}