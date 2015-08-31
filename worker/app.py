import logging
import RPi.GPIO as GPIO
from flask import Flask, jsonify, request
from logging.handlers import FileHandler
from flask.ext.sqlalchemy import SQLAlchemy

from utils import init_celery

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
celery = init_celery(app)


@app.route("/")
def index():
    try:
        result = {
            'status'    : 200,
            'result'    : 'Server working'
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
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(app.config['TERM_INPUT'], GPIO.IN)
    
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'])
