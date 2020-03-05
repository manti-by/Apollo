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
            () => this.update(), 1000
        );
    }

    render () {
        this.target.innerHTML = this.template(this.data);
    }

    update() {
        let datetime = new Date();

        this.data = {
            date: datetime.toLocaleDateString(),
            time: datetime.toLocaleTimeString()
        };
        this.render();
    };
}