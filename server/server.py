from flask import Flask, jsonify

from core.data import DB

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify(result=200, data=DB().get())
