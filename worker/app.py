import logging
from logging import FileHandler
from flask import Flask, jsonify, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template('base.html')


@app.route("/data")
def data():
    try:
        from models import Record
        record = Record.objects.order_by('-timestamp').first()
        if record:
            result = {
                'status'    : 200,
                'result'    : record._asdict()
            }
        else:
            result = {
                'status'    : 401,
                'message'   : 'There are no records found'
            }
    except Exception as e:
        result = {
            'status'    : 500,
            'message'   : e.message
        }
    return jsonify(result)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        return jsonify({
            'status'    : 500,
            'message'   : 'Not running with the Werkzeug Server'
        })

    func()
    return jsonify({
        'status'    : 200,
        'message'   : 'Server shutting down...'
    })


if __name__ == "__main__":
    log_handler = FileHandler(app.config['LOG_FILE'])
    log_handler.setLevel(logging.ERROR)
    app.logger.addHandler(log_handler)

    app.run(host=app.config['HOST'])
