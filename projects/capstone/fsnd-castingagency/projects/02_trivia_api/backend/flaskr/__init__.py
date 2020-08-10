import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import db, setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r'/*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        formatted_categories = {
            category.id: category.type for category in categories}
        return jsonify({
            'categories': formatted_categories
        })

    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]
        return jsonify({
            'questions': formatted_questions[start:end],
            'total_questions': len(questions),
            'categories': get_categories().get_json()['categories']
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get_or_404(question_id)
        question.delete()
        return jsonify({
            'success': True,
            'question_id': question_id
        })

    @app.route('/questions', methods=['POST'])
    def add_question():
        data = request.json
        try:
            question = Question(**data)
        except Exception:
            abort(400)
        question.insert()
        return jsonify({
            'success': True,
            'question_id': question.id
        })

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        search_term = request.json['search_term']
        questions = Question.query.filter(
            db.func.lower(Question.question)
            .contains(search_term.lower(), autoescape=True)
        ).all()
        formatted_questions = [question.format() for question in questions]
        return jsonify({
            'questions': formatted_questions[start:end],
            'total_questions': len(questions)
        })

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.filter_by(category=category_id).all()
        formatted_questions = [question.format() for question in questions]
        return jsonify({
            'questions': formatted_questions[start:end],
            'total_questions': len(questions)
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            previous_questions = request.json['previous_questions']
            category = int(request.json['quiz_category'])
        except Exception:
            abort(400)

        if category > 0:
            questions = Question.query.filter(
                Question.category == category
            ).filter(
                Question.id.notin_(previous_questions)
            ).all()
        else:
            questions = Question.query.filter(
                Question.id.notin_(previous_questions)
            ).all()

        questions = [question.format() for question in questions]
        question = random.choice(questions) if len(questions) > 0 else None
        return jsonify({
            'question': question
        })

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app
