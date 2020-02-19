import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  CORS(app,resources={r"/*": {"origins": "*"}})
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()

    return jsonify({
      'success': True,
      'categories': Category.to_dict(categories)
    })

  @app.route('/questions')
  def get_questions():

    page = request.args.get('page', 1, type=int)
    questions = Question.query.order_by(Question.id).paginate(page,QUESTIONS_PER_PAGE, True)
    categories = Category.query.all()

    return jsonify({
      'success': True,
      'questions': [question.format() for question in questions.items],
      'total_questions': questions.total,
      'categories': Category.to_dict(categories),
      'current_category': None
    })

  @app.route("/questions/<id>", methods=["DELETE"])
  def delete_question(id):
    question = Question.query.filter_by(id=id).one_or_none()
    
    if question is None:
      abort(422)

    question.delete()
    total_questions = Question.query.count()

    return jsonify({
      "success": True,
      "deleted_id": int(id),
      "total_questions": total_questions
    })

  @app.route("/questions", methods=["POST"])
  def create_question():

    data = request.get_json()

    if data.get("searchTerm") is None:

      new_question = Question(
        question = data.get("question"),
        answer = data.get("answer"),
        difficulty = data.get("difficulty"),
        category = data.get("category")
      )
      
      new_question.insert()

      return jsonify({
        "success": True,
        "created": new_question.id,
        "total_questions": Question.query.count()
      })
    
    else:
      search_term = data.get("searchTerm")
      questions = Question.query.filter(Question.question.ilike('%'+ search_term +'%')).all()

      return jsonify({
        "success": True,
        "questions": [question.format() for question in questions],
        "total_questions": len(questions),
        "current_category": None
      })

  @app.route('/categories/<category_id>/questions')
  def get_questions_by_category(category_id):

    category = Category.query.filter_by(id = category_id).one_or_none()

    if category is None:
      abort(404)

    questions = Question.query.filter_by(category = category_id).all()

    return jsonify({
      "success": True,
      "questions": [question.format() for question in questions],
      "total_questions": len(questions),
      "current_category": category.type
    })


  @app.route('/quizzes', methods=["POST"])
  def get_new_question_for_quiz():
    
    data = request.get_json()
    previous_questions = data.get("previous_questions")
    category = data.get("quiz_category")
    
    if(category['id'] == 0):
      question = Question.query.filter(~Question.id.in_(previous_questions)).first()
    else:
      question = Question.query.filter(Question.category == category['id'], ~Question.id.in_(previous_questions)).first()

    if question is None:
      return jsonify({
        "success": True
      })

    return jsonify({
      "success": True,
      "question": question.format()
    })

  @app.errorhandler(404)
  def page_not_found(error):
    return jsonify({
      "success": False,
      "code": 404,
      "message": "Page Not Found"
    }), 404


  @app.errorhandler(422)
  def page_not_found(error):
    return jsonify({
      "success": False,
      "code": 422,
      "message": "Request Cannot Be Processed"
    }), 422

  @app.errorhandler(405)
  def page_not_found(error):
    return jsonify({
      "success": False,
      "code": 405,
      "message": "Method Not Allowed"
    }), 405

  @app.errorhandler(500)
  def page_not_found(error):
    return jsonify({
      "success": False,
      "code": 500,
      "message": "Internal Server Error"
    }), 500

  return app

    