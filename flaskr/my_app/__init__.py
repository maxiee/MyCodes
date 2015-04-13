from flask import Flask

app = Flask(__name__)

import my_app.home.views
