from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.pagedown import PageDown

SECRET_KEY = 'wtftftftjoiduoqrwo'
app = Flask(__name__)
app.config.from_object(__name__)
pagedown = PageDown(app)
Bootstrap(app)

import my_app.home.views
