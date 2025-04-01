"""Module de vue de l'application todo"""

from flask import jsonify, abort, request, make_response
from .app import app, db
from .models import (Questionnaire,
                     Question,
                     get_un_questionnaire)

@app.errorhandler(404)
def not_found(error):
    """Fontion de gestion des erreurs 404
    Args:
        error (error): erreur
    Returns:
        [json] -- [erreur]
    """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(error):
    """Fontion de gestion des erreurs 400
    Args:
        error (error): erreur
    Returns:
        [json] -- [erreur]
    """
    return make_response(jsonify({error: "Not found"}), 400)

@app.route("/quiz/api/v1.0/questionnaires", methods=["GET"])
def get_questionnaires():
    """Fontion de récupération de tous les questionnaires
    Returns:
        [json] -- [liste des questionnaires]
    """
    return jsonify(questionnaires=[q.to_json() for q in Questionnaire.query.all()])


@app.route("/quiz/api/v1.0/questionnaires/<int:questionnaire_id>", methods=["GET"])
def get_questionnaire(questionnaire_id):
    """Fontion de récupération d'un questionnaire
    Args:
        questionnaire_id (int): identifiant du questionnaire
    Returns:
        [json] -- [questionnaire]
    """
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if questionnaire is None:
        abort(404)
    return jsonify(questionnaire.to_json())


@app.route("/quiz/api/v1.0/questionnaires", methods=["POST"])
def create_questionnaire():
    """Fontion de création d'un questionnaire
    Returns:
        [json] -- [questionnaire créé]
    """
    if not request.json or not "name" in request.json:
        abort(400)
    questionnaire = Questionnaire(request.json["name"])
    db.session.add(questionnaire)
    db.session.commit()
    return jsonify(questionnaire.to_json()), 201


@app.route("/quiz/api/v1.0/questionnaires/<int:questionnaire_id>", methods=["PUT"])
def update_questionnaire(questionnaire_id):
    """Fontion de mise à jour d'un questionnaire
    Args:
        questionnaire_id (int): identifiant du questionnaire
    Returns:
        [json] -- [questionnaire mis à jour]
    """
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if questionnaire is None:
        abort(404)
    if not request.json:
        abort(400)
    if "name" in request.json and isinstance(request.json["name"], str) is False:
        abort(400)
    questionnaire.name = request.json.get("name", questionnaire.name)
    db.session.commit()
    return jsonify(questionnaire.to_json())


@app.route("/quiz/api/v1.0/questionnaires/<int:questionnaire_id>", methods=["DELETE"])
def delete_questionnaire(questionnaire_id):
    """Fontion de suppression d'un questionnaire
    Args:
        questionnaire_id (int): identifiant du questionnaire
    Returns:
        [json] -- [message de suppression]
    """
    questionnaire = Questionnaire.query.get(questionnaire_id)
    question_associe = questionnaire.get_questions_questionnaire()
    if questionnaire is None:
        abort(404)
    if question_associe:
        for question in question_associe:
            db.session.delete(question)
    db.session.delete(questionnaire)
    db.session.commit()
    return jsonify({"result": True})


@app.route("/quiz/api/v1.0/questions", methods=["GET"])
def get_questions():
    """Fontion de récupération de toutes les questions
    Returns:
        [json] -- [liste des questions]
    """
    return jsonify(questions=[q.to_json() for q in Question.query.all()])


@app.route("/quiz/api/v1.0/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    """Fontion de récupération d'une question
    Args:
        question_id (int): identifiant de la question
    Returns:
        [json] -- [question]
    """
    question = Question.query.get(question_id)
    if question is None:
        abort(404)
    return jsonify(question.to_json())


@app.route("/quiz/api/v1.0/<int:id_questionnaire>/questions/", methods=["POST"])
def create_question(id_questionnaire):
    """Fontion de création d'une question
    Returns:
        [json] -- [question créée]
    """
    if not request.json or not "title" in request.json:
        abort(400)
    questionnaire = get_un_questionnaire(id_questionnaire)
    if questionnaire is None:
        abort(404)
    question = questionnaire.ajoute_question(request)
    return jsonify(question), 201


@app.route("/quiz/api/v1.0/questions/<int:question_id>", methods=["PUT"])
def update_question(question_id):
    """Fontion de mise à jour d'une question
    Args:
        question_id (int): identifiant de la question
    Returns:
        [json] -- [question mise à jour]
    """
    question = Question.query.get(question_id)
    if question is None:
        abort(404)
    if not request.json:
        abort(400)
    if "title" in request.json and isinstance(request.json["title"], str) is False:
        abort(400)
    question.title = request.json.get("title", question.title)
    db.session.commit()
    return jsonify(question.to_json())


@app.route("/quiz/api/v1.0/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    """Fontion de suppression d'une question
    Args:
        question_id (int): identifiant de la question
    Returns:
        [json] -- [message de suppression]
    """
    question = Question.query.get(question_id)
    if question is None:
        abort(404)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"result": True})
