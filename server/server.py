from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS

from core.database import DB
from core.conf import settings

app = Flask(__name__)
CORS(app)


@app.route('/', methods=('get',))
def index():
    return jsonify(status=200, data=DB().get())


@app.route('/search', methods=('get',))
def search():
    date_end = datetime.utcnow()
    if request.args.get('de'):
        date_end = datetime.strptime(request.args.get('de'),
                                     settings['dt_format'])

    date_start = date_end - timedelta(days=1)
    if request.args.get('ds'):
        date_start = datetime.strptime(request.args.get('ds'),
                                       settings['dt_format'])
    filters = {
        'mac': request.args.get('mac'),
        'date_start': date_start,
        'date_end': date_end,
    }
    return jsonify(status=200, data=DB().search(filters))
