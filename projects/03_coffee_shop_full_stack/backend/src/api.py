import json
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import requires_auth, AuthError

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## Routes

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    }), 200

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail():
    drinks = Drink.query.all()
    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    }), 200

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    drink_json = request.get_json()
    if any(key not in drink_json for key in ['title', 'recipe']):
        abort(400)

    for ingredient in drink_json['recipe']:
        if any(key not in ingredient for key in ['name', 'color', 'parts']):
            abort(400)

    drink = Drink(title=drink_json['title'], recipe=json.dumps(drink_json['recipe']))
    try:
        drink.insert()
    except exc.IntegrityError:
        abort(400)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200

@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(drink_id):
    drink = Drink.query.get_or_404(drink_id)
    drink_json = request.get_json()

    if 'title' in drink_json:
        drink.title = drink_json['title']
    if 'recipe' in drink_json:
        drink.recipe = drink_json['recipe']

    drink.update()
    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200

@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(drink_id):
    drink = Drink.query.get_or_404(drink_id)
    drink.delete()
    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200

## Error Handling

@app.errorhandler(400)
def bad_request(err):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400

@app.errorhandler(404)
def not_found(err):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Not Found'
    }), 404

@app.errorhandler(405)
def method_not_allowed(err):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method Not Allowed'
    }), 405

@app.errorhandler(422)
def unprocessable_entity(err):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity'
    }), 422

@app.errorhandler(500)
def server_error(err):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500

@app.errorhandler(AuthError)
def auth_error(err):
    return jsonify({
        'success': False,
        'error': err.status_code,
        'message': err.error
    }), err.status_code
