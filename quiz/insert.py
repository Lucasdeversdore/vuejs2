"""Module d'insertion de données dans la base de données de l'application todo"""

import os
from .app import app, db
from .models import (Questionnaire,
                     SimpleQuestion,
                     MultipleQuestion)


@app.cli.command()
def loaddb():
    """Fonction de chargement de la base de données"""
    print("Chargement de la base de données...")
    if os.path.exists("../quiz.db"):
        os.remove("../quiz.db")
    db.create_all()
    insert_data()
    print("Base de données chargée avec succès !")


def insert_questionnaires():
    """Fonction pour insérer des questionnaires dans la base de données"""
    # Questionnaire sur la Formule 1
    questionnaire1 = Questionnaire("Passion pour la Formule 1")
    # Questionnaire sur l'informatique
    questionnaire2 = Questionnaire("Compétences en Informatique")
    db.session.add(questionnaire1)
    db.session.add(questionnaire2)


def insert_questions():
    """Fonction pour insérer des questions dans la base de données"""
    # Questions pour le questionnaire sur la Formule 1
    questionnaire1_questions = [
        SimpleQuestion("Quelle équipe de Formule 1 préférez-vous ?",
                       "simple", 1, "Mercedes", "Ferrari"),
        SimpleQuestion(
            "Suivez-vous régulièrement les courses de Formule 1 ?", "simple", 1, "Oui", "Non"),
        SimpleQuestion("Qu'est-ce qui vous intéresse le plus dans la Formule 1 ?",
                       "simple", 1, "La vitesse", "La stratégie")
    ]
    # Questions pour le questionnaire sur l'informatique
    questionnaire2_questions = [
        SimpleQuestion("À quelle fréquence utilisez-vous un ordinateur ?",
                       "simple", 2, "Tous les jours", "Occasionnellement"),
        SimpleQuestion("Quel est votre système d'exploitation préféré ?",
                       "simple", 2, "Windows", "MacOS"),
        MultipleQuestion("Quels logiciels de développement avez-vous déjà utilisés ?",
                         "multiple", 2, "Visual Studio", "Eclipse", "PyCharm", "Sublime Text")
    ]
    # Ajout des questions à la session de la base de données
    for questions in [questionnaire1_questions, questionnaire2_questions]:
        db.session.add_all(questions)


def insert_data():
    """Fonction d'insertion de données dans la base de données"""
    insert_questionnaires()
    insert_questions()
    db.session.commit()
