class ApolloChart {

  constructor(canvas, options = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');

    this.color = 'color' in options ?
      options['color'] : 'rgba(165, 42, 42, 1)';

    this.fgcolor = 'fgcolor' in options ?
      options['fgcolor'] : 'rgba(165, 42, 42, .2)';

    this.lbcolor = 'lbcolor' in options ?
      options['lbcolor'] : 'rgba(255, 255, 255, 1)';

    this.unit = 'unit' in options ?
      options['unit'] : '';

    this.line_width = 'line_width' in options ?
      options['line_width'] : 4;

    this.font = 'font' in options ?
      options['font'] : '20px Arial';

    this.font_color = 'font_color' in options ?
      options['font_color'] : 'rgba(0, 0, 0, .9)';
  }

  draw(value) {
    let cX = Math.floor(this.canvas.width / 2),
      cY = Math.floor(this.canvas.height / 2),
      radius = Math.min(cX, cY) - this.line_width * 2,
      offset = 220 * Math.PI / 180,
      radians = value / 100 * 260 * Math.PI / 180 - offset;

    // Sensor value
    this.drawSector(cX, cY, radius, -offset, radians, this.color);

    // Fill sector
    this.drawSector(cX, cY, radius, radians, 260 * Math.PI / 180 - offset, this.fgcolor);

    // Label
    this.drawCircle(cX, cY, radius * .90, this.lbcolor);
    this.drawLabel(cX, cY, value);
  }

  drawSector(cX, cY, radius, start, stop, color) {
    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = this.line_width;
    this.ctx.lineCap = 'round';
    this.ctx.moveTo(cX, cY);
    this.ctx.beginPath();
    this.ctx.arc(cX, cY, radius, start, stop);
    this.ctx.stroke();
  }

  drawLabel(cX, cY, text) {
    this.ctx.textAlign = 'center';
    this.ctx.font = this.font;
    this.ctx.fillStyle = this.font_color;
    this.ctx.fillText(text + this.unit, cX, cY + 5);
  }

  drawCircle(cX, cY, radius, color) {
    this.ctx.fillStyle = color;
    this.ctx.shadowColor = 'rgb(0, 0, 0, .2)';
    this.ctx.shadowOffsetX = 0;
    this.ctx.shadowOffsetY = 1;
    this.ctx.shadowBlur = 2;
    this.ctx.beginPath();
    this.ctx.moveTo(cX, cY);
    this.ctx.arc(cX, cY, radius, 0, 360 * Math.PI / 180);
    this.ctx.closePath();
    this.ctx.fill();
  }
}
