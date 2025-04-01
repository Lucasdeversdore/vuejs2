"""Module de l'application quizz"""

import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
CORS(app)

def mkpath(path):
    """Fonction de création d'un chemin absolu
    Args:
        path (str): chemin relatif
    Returns:
        str: chemin absolu
    """
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__), path))

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + mkpath('../quiz.db'))
db = SQLAlchemy(app)
