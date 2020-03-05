from time import localtime, strftime

from flask import Flask, jsonify, render_template, request
from flask_static_compress import FlaskStaticCompress

from apollo.database.sensors import get_sensors_data
from apollo.database.currency import get_currency_data

app = Flask(__name__)
compress = FlaskStaticCompress(app)


@app.route("/", methods=["GET"])
def index():
    limit = request.args.get("limit", 10)
    group = request.args.get("group", "hourly")
    data = get_sensors_data(limit, group)
    return render_template(
        "index.html", data=data, options={'limit': limit, 'group': group}, time=strftime("%H:%M", localtime())
    )


@app.route("/api/sensors/", methods=["GET"])
def get_sensors_api():
    limit = request.args.get("limit", 10)
    group = request.args.get("group", "hourly")
    return jsonify(get_sensors_data(limit, group))


@app.route("/api/currency/", methods=["GET"])
def get_currency_api():
    limit = request.args.get("limit", 10)
    group = request.args.get("group", "hourly")
    return jsonify(get_currency_data(limit, group))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
