"""Module du modèle de données de l'application todo"""
from .app import db


class Questionnaire(db.Model):
    """Classe de modèle de données d'un questionnaire

    Args:
        db (object): objet de connexion à la base de données

    Returns:
        object: objet de modèle de données d'un questionnaire
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        """Constructeur de la classe

        Args:
            name (str): nom du questionnaire
        """
        self.name = name

    def __repr__(self):
        """Fonction de représentation de la classe

        Returns:
            str: représentation de la classe
        """
        return f"<Questionnaire ({self.id}) {self.name}>"

    def to_json(self):
        """Fonction de conversion de la classe en JSON

        Returns:
            json: représentation JSON de la classe
        """
        json = {
            "id": self.id,
            "name": self.name,
            "questions": [q.to_json() for q in self.questions]
        }
        return json

    def get_questions_questionnaire(self):
        """Fonction de récupération des questions associées au questionnaire

        Returns:
            list: liste des questions associées au questionnaire
        """
        return Question.query.filter_by(questionnaire_id=self.id).all()

    def ajoute_question(self, request):
        """Fonction d'ajout d'une question au questionnaire
        Args:
            request (object): objet de requête
        Returns:
            object: objet de modèle de données d'une question
        """
        if request.json.get("question_type") == "simple":
            print(request.json.get("question"))
            question = SimpleQuestion(title=request.json.get("title"),
                                      question_type=request.json.get(
                                          "question_type"),
                                      questionnaire_id=self.id,
                                      choix1=request.json.get(
                                          "question")["choix1"],
                                      choix2=request.json.get("question")["choix2"])
        elif request.json.get("question_type") == "multiple":
            question = MultipleQuestion(title=request.json.get("title"),
                                        question_type=request.json.get(
                                            "question_type"),
                                        questionnaire_id=self.id,
                                        choix1=request.json.get(
                                            "question")["choix1"],
                                        choix2=request.json.get(
                                            "question")["choix2"],
                                        choix3=request.json.get(
                                            "question")["choix3"],
                                        choix4=request.json.get("question")["choix4"])
        else:
            question = Question(title=request.json.get("title"),
                                question_type=request.json.get(
                                    "question_type"),
                                questionnaire_id=self.id)
        db.session.add(question)
        db.session.commit()
        return question.to_json()


class Question(db.Model):
    """Classe de modèle de données d'une question
    Args:
        db (object): objet de connexion à la base de données
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    question_type = db.Column(db.String(120))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey("questionnaire.id"))

    questionnaire = db.relationship("Questionnaire",
                                    backref=db.backref("questions", lazy="dynamic"))
    __mapper_args__ = {
        'polymorphic_identity': 'question',
        'polymorphic_on': question_type
    }

    def __init__(self, title, question_type, questionnaire_id):
        """Constructeur de la classe
        Args:
            title (str): titre de la question
            questionType (str): type de la question
            questionnaire_id (int): identifiant du questionnaire
        """
        self.title = title
        self.question_type = question_type
        self.questionnaire_id = questionnaire_id

    def __repr__(self):
        """Fonction de représentation de la classe
        Returns:
            str: représentation de la classe
        """
        return f"<Question ({self.id}) {self.title}>"

    def to_json(self):
        """Fonction de conversion de la classe en JSON
        Returns:
            json: représentation JSON de la classe
        """
        return {
            "id": self.id,
            "title": self.title,
            "question_type": self.question_type,
            "questionnaire_id": self.questionnaire_id,
            "question": self.content()
        }


class SimpleQuestion(Question):
    """Classe de modèle de données d'une question simple
    Args:
        Question (object): objet de modèle de données d'une question
    """
    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    choix1 = db.Column(db.String(120))
    choix2 = db.Column(db.String(120))
    __mapper_args__ = {
        'polymorphic_identity': 'simple',
    }

    def content(self):
        """Fonction de récupération du contenu de la question

        Returns:
            dict: contenu de la question
        """
        return {"choix1": self.choix1, "choix2": self.choix2}

    def __init__(self, title, question_type, questionnaire_id, choix1="", choix2=""):
        """Constructeur de la classe
        Args:
            title (str): titre de la question
            question_type (str): type de la question
            questionnaire_id (int): identifiant du questionnaire
            question (str): question
        """
        super().__init__(title, question_type, questionnaire_id)
        self.choix1 = choix1
        self.choix2 = choix2


class MultipleQuestion(Question):
    """Classe de modèle de données d'une question multiple
    Args:
        Question (object): objet de modèle de données d'une question
    """
    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    choix1 = db.Column(db.String(120))
    choix2 = db.Column(db.String(120))
    choix3 = db.Column(db.String(120))
    choix4 = db.Column(db.String(120))
    __mapper_args__ = {
        'polymorphic_identity': 'multiple',
    }

    def content(self):
        """Fonction de récupération du contenu de la question

        Returns:
            dict: contenu de la question
        """
        return {"choix1": self.choix1,
                "choix2": self.choix2,
                "choix3": self.choix3,
                "choix4": self.choix4}

    def __init__(self, title, question_type, questionnaire_id,
                 choix1="", choix2="", choix3="", choix4=""):
        """Constructeur de la classe
        Args:
            title (str): titre de la question
            question_type (str): type de la question
            questionnaire_id (int): identifiant du questionnaire
            question (str): question
        """
        super().__init__(title, question_type, questionnaire_id)
        self.choix1 = choix1
        self.choix2 = choix2
        self.choix3 = choix3
        self.choix4 = choix4


def get_max_id(table):
    """Fonction de récupération de l'identifiant maximum d'une table
    Args:
        table (object): objet de modèle de données d'une table

    Returns:
        int: identifiant maximum de la table
    """
    max_id = db.session.query(db.func.max(table.id)).scalar()
    if max_id is None:
        max_id = 0
    return max_id


def get_un_questionnaire(questionnaire_id):
    """Fonction de récupération d'un questionnaire
    Args:
        questionnaire_id (int): identifiant du questionnaire

    Returns:
        object: objet de modèle de données d'un questionnaire
    """
    return Questionnaire.query.get(questionnaire_id)
