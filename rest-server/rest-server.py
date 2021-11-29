from werkzeug.wrappers import response
from flask import Flask, request, Response
import redis
import json
import jsonpickle
import pika

from flask import render_template, flash, redirect, request, make_response, Response

# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

@app.route('/')
def root():
    return "<p>Hello, World!</p>"



# start flask app
app.run(host="0.0.0.0", port=5000)
