#!/bin/bash

# Créer un environnement virtuel
virtualenv -p python3 venv

# Activer l'environnement virtuel
source ./venv/bin/activate

# Installer les dépendances depuis requirements.txt
pip install -r ./requirements.txt

# Naviguer vers le répertoire du quiz
cd ./quiz/

# Charger la base de données
flask loaddb

# Lancer le serveur
flask run
