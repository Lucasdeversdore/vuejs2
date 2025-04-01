# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Installer les dépendances depuis requirements.txt
pip install -r .\requirements.txt

# Naviguer vers le répertoire du quiz
cd .\quiz\

# Charger la base de données
flask loaddb

# Lancer le serveur
flask run
