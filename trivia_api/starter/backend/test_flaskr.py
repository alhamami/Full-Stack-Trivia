import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category




def assertPage(self,ques,jsPage,lnth):
    status = ques.status_code
    self.assertEqual(status, 200)
    self.assertEqual(jsPage['success'], True)
    self.assertTrue(jsPage['total_questions'])
    self.assertTrue(lnth)


def errorPage(self,statusError,jsError404):
    self.assertEqual(statusError, 404)
    self.assertEqual(jsError404['success'], False)
    self.assertEqual(jsError404['message'], 'resource not found')


def assertQ(self, cancelQues, jsQ, getQ, getQ2, getQ3):
    self.assertEqual(self.client().delete('/questions/{}'.format(cancelQues.id)).status_code, 200)
    self.assertEqual(jsQ['success'], True)
    self.assertEqual(jsQ['deleted'], id)
    lenq1 = len(getQ)
    lenq2 = len(getQ2)
    lenResult = lenq1 - lenq2
    self.assertTrue( lenResult == 1)
    self.assertEqual(getQ3, None)


def assertMakeQ(self, jsMakeQ, makeQ1, makeQ2, getMQ):
    mQStatus = self.client().post('/questions', json=self.new_question).status_code
    self.assertEqual(mQStatus, 200)
    self.assertEqual(jsMakeQ['success'], True)
    mQLen1 = len(makeQ1)
    mQLen2 = len(makeQ2)
    self.assertTrue(mQLen2 - mQLen1 == 1)
    self.assertIsNotNone(getMQ)


def assertError422(self, jsError422, error422Q1, error422Q2):
    errorStatus = self.client().post('/questions', json={}).status_code
    self.assertEqual(errorStatus, 422)
    self.assertEqual(jsError422['success'], False)
    lenError1 = len(error422Q1)
    lenError2 = len(error422Q2)
    self.assertTrue(lenError2 == lenError1 )


def searchQ(self, searchQStatus, jsSearchQ):
    self.assertEqual(searchQStatus, 200)
    self.assertEqual(jsSearchQ['success'], True)
    lenSQ = len(jsSearchQ['questions'])
    self.assertEqual(lenSQ, 1)
    self.assertEqual(jsSearchQ['questions'][0]['id'], 23)   


def search404(self, jsSearch404):
    search404Status = self.client().post('/questions',json={'searchTerm': 'abcdefghijk'}).status_code
    self.assertEqual(search404Status, 404)
    self.assertEqual(jsSearch404['success'], False)
    self.assertEqual(jsSearch404['message'], 'resource not found')


def categoryQues(self, jsCategoryQ):
    categoryQuesStatus = self.client().get('/categories/1/questions').status_code
    self.assertEqual(categoryQuesStatus, 200)
    self.assertEqual(jsCategoryQ['success'], True)
    self.assertNotEqual(len(jsCategoryQ['questions']), 0)
    self.assertEqual(jsCategoryQ['current_category'], 'Science')


def categor404Q(self, jsCategor404):
    self.assertEqual(self.client().get('/categories/100/questions').status_code, 400)
    self.assertEqual(jsCategor404['success'], False)
    self.assertEqual(jsCategor404['message'], 'bad request')


 
def quizQues(self, jsQuizQ):
    self.assertEqual(self.client().post('/quizzes',json={'previous_questions': [20, 21],'quiz_category': {'type': 'Science', 'id': '1'}}).status_code, 200)
    self.assertEqual(jsQuizQ['success'], True)
    self.assertTrue(jsQuizQ['question'])
    self.assertEqual(jsQuizQ['question']['category'], 1)
    self.assertNotEqual(jsQuizQ['question']['id'], 20)
    self.assertNotEqual(jsQuizQ['question']['id'], 21)


def quizErrorQ(self, jsQuizError):
    quizErrorStatus = self.client().post('/quizzes', json={}).status_code
    self.assertEqual(quizErrorStatus, 400)
    self.assertEqual(jsQuizError['success'], False)
    self.assertEqual(jsQuizError['message'], 'bad request')





class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://postgres:123123@localhost:5432/trivia_test'
        setup_db(self.app, self.database_path)
############################################################

        self.new_question = {'question': 'What is your name?',
            'answer': 'Jalal','difficulty': 2,'category': '1'}

############################################################

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

#################################################################

    def test_error_404(self):
        ques404 = self.client().get('/questions?page=100')
        jsError = ques404.data
        jsError404 = json.loads(jsError)
        statusError = ques404.status_code
        errorPage(self,statusError,jsError404)
        

#################################################################


    def test_page(self):

        ques = self.client().get('/questions')
        jsDataPage = ques.data
        jsPage = json.loads(jsDataPage)
        lnth = len(jsPage['questions'])
        assertPage(self,ques,jsPage,lnth)    


################################################################## 


    def test_quizError(self):
        jsQuizError = json.loads(self.client().post('/quizzes', json={}).data)
        quizErrorQ(self, jsQuizError)


################################################################  

    def test_makeQ(self):
        makeQ1 = Question.query.all()
        jsMakeQ = json.loads(self.client().post('/questions', json=self.new_question).data)
        makeQ2 = Question.query.all()
        getMQ = Question.query.filter_by(id=jsMakeQ['created']).one_or_none()
        assertMakeQ(self, jsMakeQ, makeQ1, makeQ2, getMQ)


###############################################################  

    def test_categor404(self):

        jsCategor404= json.loads(self.client().get('/categories/100/questions').data)
        categor404Q(self, jsCategor404)
   


###############################################################  


    def test_cancelQ(self):

        qx = self.new_question['question']
        qy = self.new_question['answer']
        qz = self.new_question['category']
        qw = self.new_question['difficulty']
        cancelQues = Question(question=qx, answer=qy,category=qz , difficulty=qw)
        cancelQues.insert()
        getQ = Question.query.all()
        jsQ = json.loads(self.client().delete('/questions/{}'.format(cancelQues.id)).data)
        getQ2 = Question.query.all()
        getQ3 = Question.query.filter(Question.id == 1).one_or_none()
        assertQ(self, cancelQues, jsQ, getQ, getQ2, getQ3)     

############################################################### 

    def test_search404Q(self):

        jsSearch404 = json.loads(self.client().post('/questions',json={'searchTerm': 'abcdefghijk'}).data)
        search404(self, jsSearch404)


###############################################################   


    def test_categoryQ(self):
        jsCategoryQ = json.loads(self.client().get('/categories/1/questions').data)
        categoryQues(self, jsCategoryQ)


###############################################################   


    def test_searchQ(self):

        jsSearchQ = json.loads(self.client().post('/questions',json={'searchTerm': 'egyptians'}).data)
        searchQStatus = self.client().post('/questions',json={'searchTerm': 'egyptians'}).status_code
        searchQ(self, searchQStatus, jsSearchQ)

###############################################################  


    def test_quizQ(self):
        jsQuizQ = json.loads(self.client().post('/quizzes',json={'previous_questions': [20, 21],'quiz_category': {'type': 'Science', 'id': '1'}}).data)
        quizQues(self, jsQuizQ)



###############################################################    

    def test_error422(self):

        error422Q1 = Question.query.all()
        jsError422 = json.loads(self.client().post('/questions', json={}).data)
        error422Q2 = Question.query.all()
        assertError422(self, jsError422, error422Q1, error422Q2)





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
