document.addEventListener("DOMContentLoaded", () => {
    let currency = new CurrencyWidget();
    currency.init();

    let datetime = new DatetimeWidget();
    datetime.init();

    let weather = new WeatherWidget();
    weather.init();

    let indoor_climate = new IndoorClimateWidget();
    indoor_climate.init();

    let indoor_climate_report = new IndoorClimateReportWidget();
    indoor_climate_report.init();
});
