from flask import Flask
import os

from main.views import main_blueprint
from loader.views import loader_blueprint


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'SuperSecretKey'

# вызываем блупринты
app.register_blueprint(main_blueprint)
app.register_blueprint(loader_blueprint)
