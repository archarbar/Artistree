from flask import Flask

app = Flask(__name__)

from src.views import main
