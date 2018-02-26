from flask import Flask, jsonify

from app.db import DB

app = Flask(__name__)


@app.route('/')
def index():
    db = DB()
    data = db.get()
    return jsonify(result=200, data=data)
