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
            () => this.update(), 60 * 1000
        );
    }

    render () {
        this.target.innerHTML = this.template(this.data);
    }

    update() {
        let datetime = new Date();

        this.data = {
            date: datetime.getDate() + '-' + datetime.getMonth() + 1  + '-' + datetime.getFullYear(),
            time: datetime.getHours() + '<span class="separator">:</span>' + datetime.getMinutes(),
        };
        this.render();
    };
}