from time import localtime, strftime

from flask import Flask, jsonify, render_template, request
from flask_static_compress import FlaskStaticCompress

from app.database import get_data

app = Flask(__name__)
compress = FlaskStaticCompress(app)


@app.route("/")
def index():
    data, options = get_data()
    return render_template(
        "index.html", data=data, options=options, time=strftime("%H:%M", localtime())
    )


@app.route("/api", methods=["GET", "POST"])
def api():
    if request.method == "GET":
        return jsonify(get_data()[0])
    else:
        return jsonify("OK")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
