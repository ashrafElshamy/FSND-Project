import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import random
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','2021','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_all(self):
        res = self.client().get("/")
        self.assertEqual(res.status_code, 404)

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertTrue(len(data['questions'])
    
    def test_get_questions(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_questions_fail(self):
        res = self.client().get("/categories/5000000/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_question_search(self):
        newSearch = {
            "searchTerm":""
        }
        res = self.client().post("/questions/search", json=newSearch)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertTrue(len(data['questions'])
    
    def test_questions(self):
        newQuizze = {
            "quiz_category":""
        }
        res = self.client().post("/quizzes", json=newQuizze)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        # self.assertTrue(len(data['questions'])

    def test_delete_question(self):
        res = self.client().delete("/questions/10000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
    
    # def test_delete_question(self):
    #     res = self.client().delete("/questions/4")
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)



    def test_create_question(self):
        new_question = "new question" + str(random.randint(0, 999999999))
        new_answer = ""
        new_category = 1
        new_difficulty = 1

        newQuestion = {
            "question":new_question,
            "answer":new_answer,
            "category":new_category,
            "difficulty":new_difficulty
        }

        # 1) valid data
        res = self.client().post("questions/add", json=newQuestion)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        inserted_question = Question.query.order_by(self.db.desc(Question.id)).first()
        self.assertTrue(inserted_question)
        self.assertEqual(inserted_question.question, new_question)
        self.assertEqual(inserted_question.category, new_category)
        self.assertEqual(inserted_question.id, data["created_question"])

        # 2)missing question
        newQuestion = {
            "category": new_category
        }
        res = self.client().post("questions/add", json=newQuestion)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 500)
        self.assertEqual(data['message'], "Error while tring to add new question")

        
        # empty request
        newQuestion = {
            "question": "",
            "category": new_category
        }
        res = self.client().post("questions/add", json=newQuestion)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "Error while tring to add new question")
    
   

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()