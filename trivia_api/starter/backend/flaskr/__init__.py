import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def quesF(one):
    return [question.format() for question in one]

def bLimit(init):
    sQPS = (init - 1) * QUESTIONS_PER_PAGE
    beg = sQPS
    return beg
    
def fLimit(b):
    eQPS = b + QUESTIONS_PER_PAGE
    fin = eQPS
    return fin

def orderP(get,one):
    init = get.args.get('page', 1, type=int)
    all = quesF(one)
    b = bLimit(init)
    f = fLimit(b)
    nQ = all[b:f]
    return nQ

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={'/': {'origins': '*'}})

    @app.after_request
    def dec(info):
        info.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
        info.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
        return info

    def all_e():
        each_CTGS = Category.query.all()
        each = {}
        for cTmp in each_CTGS:
            cType = cTmp.type
            x = cTmp.id
            each[x] = cType

        return each

    def all_CTGS(CTGS):
        CTGS_Json = CTGS
        x = jsonify({'success': True,'categories': CTGS_Json})
        return x    

    def len_CTGS(CTGS):
        lenCTGS = len(CTGS)
        if (lenCTGS == 0):
            abort(404)

    @app.route('/categories')
    def each():
        CTGS = all_e()
        len_CTGS(CTGS)
        return all_CTGS(CTGS)

    def CTGS_q_1():
        CTGS_q_1_x = Question.query.all()
        CTGS_q_1_y = len(CTGS_q_1_x)
        return CTGS_q_1_y

    def CTGS_q_2():
        CTGS_q_2_x = Question.query.all()
        CTGS_q_2_y = orderP(request, CTGS_q_2_x)
        return CTGS_q_2_y

    def CTGS_q_3():
        CTGS_q_3_x = len(CTGS_q_2())
        if ( CTGS_q_3_x == 0):
            abort(404)

    def CTGS_q_4():
        CTGS_q_4_y = {}
        CTGS_q_4_x = Category.query.all()
        for x in CTGS_q_4_x:
            CTGS_q_4_type = x.type
            CTGS_q_4_id = x.id
            CTGS_q_4_y[CTGS_q_4_id] = CTGS_q_4_type
        return CTGS_q_4_y

    @app.route('/questions')
    def CTGS_q():
        CTGS_q_3()
        return jsonify({'success': True,'questions': CTGS_q_2(),'total_questions': CTGS_q_1(),'categories': CTGS_q_4()})


    def CTGS_del_1():
        CTGS_del_1_Tmp = Question.query.filter_by(id=id).one_or_none()
        if CTGS_del_1 is None:
                abort(404)
        else:    
         CTGS_del_1.delete()

    def CTGS_del_2():
        abort(422)

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def CTGS_del(id):
        try:
            CTGS_del_1()
            return jsonify({'success': True,'deleted': id})
        except:
            CTGS_del_2()


    def CTGS_New_1(CTGS_New_Tmp2):
        CTGS_New_1_Tmp = Question.query.filter(Question.question.ilike(
            f'%{CTGS_New_Tmp2}%')).all()

        return CTGS_New_1_Tmp


    def CTGS_New_2(CTGS_New_Tmp3):
        CTGS_New_2_Tmp = len(CTGS_New_Tmp3)
        if ( CTGS_New_2_Tmp == 0):
            abort(404)

    def CTGS_New_3(CTGS_New_Tmp1):
        if (CTGS_New_Tmp1.get('question') is None):
            abort(422)
        if(CTGS_New_Tmp1.get('answer') is None):
            abort(422)
        if(CTGS_New_Tmp1.get('difficulty') is None):
            abort(422)
        if(CTGS_New_Tmp1.get('category') is None):
            abort(422)


    def CTGS_New_4(CTGS_New_Tmp1):
        CTGS_New_4_Tmp = Question(question=CTGS_New_Tmp1.get('question'), answer=CTGS_New_Tmp1.get('answer'),
        difficulty=CTGS_New_Tmp1.get('difficulty'), category=CTGS_New_Tmp1.get('category'))
        return CTGS_New_4_Tmp



    def CTGS_New_5():
        CTGS_New_5_Tmp = orderP(request, Question.query.order_by(Question.id).all())  
        return CTGS_New_5_Tmp
        

    @app.route('/questions', methods=['POST'])
    def CTGS_New():
        
        CTGS_New_Tmp1 = request.get_json()
        ter = 'searchTerm'
        if (CTGS_New_Tmp1.get(ter)):
            CTGS_New_Tmp2 = CTGS_New_Tmp1.get(ter)

            CTGS_New_Tmp3 = CTGS_New_1(CTGS_New_Tmp2)
            CTGS_New_2(CTGS_New_Tmp3)
            CTGS_New_que = orderP(request, CTGS_New_Tmp3)
            CTGS_New_nm = len(Question.query.all())

            return jsonify({'success': True,'questions': CTGS_New_que,
            'total_questions': CTGS_New_nm})

        else:
            CTGS_New_3(CTGS_New_Tmp1)

            try:
    
                CTGS_New_q = CTGS_New_4(CTGS_New_Tmp1)
                CTGS_New_q.insert()

                CTGS_New_n = CTGS_New_5()

                CTGS_New_Len = len(Question.query.all())
                return jsonify({'success': True,'created': CTGS_New_q.id,
                    'question_created': CTGS_New_q.question,'questions': CTGS_New_n,
                    'total_questions': CTGS_New_Len})

            except:
                abort(422)

    def CTGS_all_q_1(CTGS_all_q_Tmp2):
 
        selection = Question.query.filter_by(category=CTGS_all_q_Tmp2.id).all()
        return selection

    @app.route('/categories/<int:id>/questions')
    def CTGS_all_q(id):
        CTGS_all_q_Tmp1 = len(Question.query.all())
        CTGS_all_q_Tmp2 = Category.query.filter_by(id=id).one_or_none()
        if (CTGS_all_q_Tmp2 is None):
            abort(400)

        return jsonify({'success': True,'questions': orderP(request, CTGS_all_q_1(CTGS_all_q_Tmp2)),
            'total_questions': CTGS_all_q_Tmp1,'current_category': CTGS_all_q_Tmp2.type })


    def CTGS_Quizzes_1(CTGS_Quizzes_Tmp1):
        
        if (CTGS_Quizzes_Tmp1.get('quiz_category') is None):
            abort(400)
        if (CTGS_Quizzes_Tmp1.get('previous_questions') is None):
            abort(400)


    def CTGS_Quizzes_2(CTGS_Quizzes_Tmp1):
        if (CTGS_Quizzes_Tmp1.get('quiz_category')['id'] == 0):
            CTGS_Quizzes_2_tmp1 = Question.query.all()
        else:
            CTGS_Quizzes_2_tmp1 = Question.query.filter_by(category=CTGS_Quizzes_Tmp1.get('quiz_category')['id']).all()

        return CTGS_Quizzes_2_tmp1




    @app.route('/quizzes', methods=['POST'])
    def CTGS_Quizzes():

        CTGS_Quizzes_Tmp1 = request.get_json()
        CTGS_Quizzes_1(CTGS_Quizzes_Tmp1)
        CTGS_Quizzes_Tmp2 = CTGS_Quizzes_2(CTGS_Quizzes_Tmp1)

        def CTGS_Quizzes_3():
            CTGS_Quizzes_3_tmp = len(CTGS_Quizzes_Tmp2)
            CTGS_Quizzes_3_tmp = CTGS_Quizzes_Tmp2[random.randrange(0, CTGS_Quizzes_3_tmp, 1)]
            return CTGS_Quizzes_3_tmp

        def CTGS_Quizzes_4(question):
            CTGS_Quizzes_4_x = False
            for q in CTGS_Quizzes_Tmp1.get('previous_questions'):
                if (q == question.id):
                    CTGS_Quizzes_4_x = True
            return CTGS_Quizzes_4_x

        question = CTGS_Quizzes_3()
        while (CTGS_Quizzes_4(question)):
            question = CTGS_Quizzes_3()
            CTGS_Quizzes_l = len(CTGS_Quizzes_Tmp1.get('previous_questions'))
            CTGS_Quizzes_ll = len(CTGS_Quizzes_Tmp2)
            if ( CTGS_Quizzes_l == CTGS_Quizzes_ll):
                return jsonify({'success': True})

        CTGS_Quizzes_f = question.format()
        return jsonify({'success': True,'question': CTGS_Quizzes_f})



    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False,"error": 404,"message": "resource not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False,"error": 422,"message": "unprocessable"}), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False,"error": 400,"message": "bad request"}), 400

    return app



if __name__ == "__main__":
    create_app().run(debug=True)