from flask import Flask

app = Flask(__name__)

from application.main.views import main

app.register_blueprint(main)