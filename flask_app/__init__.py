from flask import Flask #importamos flask

app = Flask(__name__)#inicializamos app

app.secret_key = "Llave secreta!" #se necesita para la sesión, es la manera en que se encripta
