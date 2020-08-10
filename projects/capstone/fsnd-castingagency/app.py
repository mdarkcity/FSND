import os
import datetime
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import requires_auth, AuthError


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Routes

    @app.route('/movies')
    @requires_auth('view:movies')
    def get_movies():
        movies = Movie.query.all()
        return jsonify({
            'movies': [movie.format() for movie in movies]
        })

    @app.route('/actors')
    @requires_auth('view:actors')
    def get_actors():
        actors = Actor.query.all()
        return jsonify({
            'actors': [actor.format() for actor in actors]
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movie')
    def create_movie():
        movie_json = request.get_json()

        if movie_json is None:
            abort(400)
        if movie_json.keys() != set(['title', 'release_date']):
            abort(400)
        if None in movie_json.values():
            abort(400)

        title = movie_json['title']
        release_date = stringToDate(movie_json['release_date'])

        movie = Movie(title, release_date)
        movie.insert()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actor')
    def create_actor():
        actor_json = request.get_json()

        if actor_json is None:
            abort(400)
        if actor_json.keys() != set(['name', 'age', 'gender'])\
                and actor_json.keys() != set(['name', 'age']):
            abort(400)
        if None in actor_json.values():
            abort(400)

        actor = Actor(**actor_json)
        actor.insert()
        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('modify:movie')
    def update_movie(movie_id):
        movie = Movie.query.get_or_404(movie_id)
        movie_json = request.get_json()

        if 'title' in movie_json:
            movie.title = movie_json['title']
        if 'release_date' in movie_json:
            movie.release_date = stringToDate(movie_json['release_date'])

        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('modify:actor')
    def update_actor(actor_id):
        actor = Actor.query.get_or_404(actor_id)
        actor_json = request.get_json()

        if 'name' in actor_json:
            actor.name = actor_json['name']
        if 'age' in actor_json:
            actor.age = actor_json['age']
        if 'gender' in actor_json:
            actor.gender = actor_json['gender']

        actor.update()
        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(movie_id):
        movie = Movie.query.get_or_404(movie_id)
        movie.delete()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(actor_id):
        actor = Actor.query.get_or_404(actor_id)
        actor.delete()
        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    # Helper Methods

    def stringToDate(date_string):
        date_parts = date_string.split('-')
        return datetime.date(*[int(part) for part in date_parts])

    # Error Handlers

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

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
