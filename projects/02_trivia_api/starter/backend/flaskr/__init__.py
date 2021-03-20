import os
from flask import Flask, request, abort, jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
import random
from models import Question,Category,db
from werkzeug.exceptions import HTTPException

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response     


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def getAllCat():
        categories = Category.query.order_by(Category.id).all()
        return jsonify({
          "success":True,
          "question": "",
          "answer": "",
          "difficulty": 1,
          "category": 1,
          "categories":format_cat(categories)})


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
  def paginate_questions(request,selection):
    page = request.args.get('page',1,type=int)
    start = (page - 1) * 10
    end   = start+10
    questions =  [question.format() for question in selection]
    current_qu =  questions[start:end]
    return  current_qu

  def format_cat(cat):
        obj= {}
        for catig in cat:
          obj[catig.id] = catig.type       
        return obj

  @app.route('/questions')
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request,selection)

    categories = Category.query.order_by(Category.id).all()
    if selection is None:
      abort(404)

    return jsonify({
       "success":True,
       "questions":current_questions,
       "categories":format_cat(categories),
       "current_category":"",
       "total_questions":len(selection)
    })   

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:q_id>', methods=['DELETE'])
  def delete_question(q_id):
    error = False    
    try:
      question  = Question.query.filter(Question.id==q_id).one_or_none()
      if question is None:
          error = True
          error_code = 422
      else:
        question.delete()
 
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request,selection)
    except:
      error_code = 422
      error = True
      db.session.rollback()
    finally:
      db.session.close()
      if error:
            raise myException(
            error_code, "the question you're trying to delete does not exist")
      else:
          return jsonify({
              "success":True,
              "deleted_question":q_id,
              "questions":current_questions,
              "total_questions":len(selection)
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
  @app.route('/questions/add', methods=['POST'])
  def add_question():
    error = False
    body = request.get_json()
    print(body)
    new_question =body.get('question',None)
    new_answer = body.get('answer',None)
    new_category = body.get('category',None)
    new_difficulty =body.get('difficulty',None)
    try:
      if new_question is None:
        error = True
        error_code = 422 
      if len(new_question)==0:
         error = True
         error_code = 422  

      question = Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request,selection)
 
      if selection is None:
        error = True
        error_code = 500
      
 
      return jsonify({
        "success":True,
        "created_question":question.id,
        "questions":current_questions,
        "total_questions":len(selection)
      })
    except:
      error = True
      error_code = 500
      db.session.rollback()
    finally:
      db.session.close()
      if error:
            raise myException(
            error_code, "Error while tring to add new question")


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_question():
    body = request.get_json()
    new_id = body.get('searchTerm',None)
    selection = Question.query.filter(func.lower(Question.question).contains(func.lower(new_id))).all() 
    current_questions = paginate_questions(request,selection)
    sq = db.session.query(Question.category).subquery()
    categories = Category.query.filter(Category.id.in_(sq)).order_by(Category.id).all()
    if selection is None:
      abort(404)

    return jsonify({
       "success":True,
       "questions":current_questions,
       "categories":format_cat(categories),
       "current_category":"",
       "total_questions":len(selection)
    })    
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:cat_id>/questions')
  def get_by_cat_id(cat_id):
    error = False
    selection = Question.query.filter(Question.category==cat_id).all()
    current_questions = paginate_questions(request,selection)
    if len(selection)==0:
          error = True
          error_code = 404
    print(selection)
    if error:
            raise myException(
              error_code, "no questions find") 
    else:  
      return jsonify({
         "success":True,
         "questions":current_questions,
         "current_category":cat_id,
         "total_questions":len(selection)
      })   

        

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
  @app.route('/quizzes', methods=['POST'])
  def cat_quizz():
    error = False
    obj = {}
    q = []
    try:
      body = request.get_json()
      previous_questions = body.get('previous_questions')
      for questions in previous_questions:
        q.append(questions('id'))      
      print("val"+ str(q))
      quiz_category = body.get('quiz_category')
      print(quiz_category) 
      if quiz_category['id'] is None:
          error_code = 500
          error = True
      question = Question.query.filter(Question.category==quiz_category['id'],Question.id.notin_(q)).order_by(func.random()).limit(1) \
             .all()
      for q in  question:      
        obj = q.format()
      categories = Category.query.order_by(Category.id).all()
      print(obj)
      return jsonify({
           "success":True,
           "quizCategory":"",
           "previousQuestions": previous_questions,
           "showAnswer": False,
           "numCorrect": "0",
           "currentQuestion": obj,
           "categories":format_cat(categories),
           "guess":"",
           "forceEnd":False
           })
    except:
      error = True
      error_code = 500
      db.session.rollback()
    finally:
      db.session.close()
      if error:
            raise myException(
            error_code, "quizze error")

       
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  class myException(Exception):
    def __init__(self, code, name):
        self.code = code
        self.name = name

  @app.errorhandler(myException)
  def genericErrorHandler(e):
      return jsonify({
        "success":False,
        "error": e.code,
        "message": e.name
      }), e.code
  @app.errorhandler(400)
  def no_datafound(error):
       return jsonify({
         "success":False,
         "error":400,
         "message":"Bad Request"
       }) ,400

  @app.errorhandler(404)
  def no_datafound(error):
       return jsonify({
         "success":False,
         "error":404,
         "message":"no resource found"
       }) ,404
  
  @app.errorhandler(422)
  def unprocessable(error):
       return jsonify({
         "success":False,
         "error":422,
         "message":"unprocessable"
       }) ,422
  
  
  return app

    