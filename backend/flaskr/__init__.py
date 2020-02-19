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
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app,resources={r"/*": {"origins": "*"}})
  

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()

    return jsonify({
      'success': True,
      'categories': Category.to_dict(categories)
    })
  
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

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


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
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

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route("/questions", methods=["POST"])
  def create_question():

    data = request.get_json()
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

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

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

  return app

    