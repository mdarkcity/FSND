# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Documentation

### Pagination

By default, all endpoints implementing pagination return 10 questions per page. The page number is specified as a query parameter: e.g., `?page=1`

### Endpoints

[`GET /categories`](####GET-/categories)\
[`GET /categories/<category_id>/questions`](####GET-/categories/<category_id>/questions)\
[`GET /questions`](####GET-/questions)\
[`POST /questions`](####POST-/questions)\
[`DELETE /questions/<question_id>`](####DELETE-/questions/<question_id>)\
[`POST /questions/search`](####POST-/questions/search)\
[`POST /quizzes`](####POST-/quizzes)

#### GET /categories
- Fetch all available trivia categories
- Request arguments: None
- Returns: An object with a single key (categories) mapping to an object of id: category_string key-value pairs
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    ...
  }
}
```

#### GET /categories/\<category_id\>/questions
- Fetch questions by category
- Request arguments:
    - Query parameters: `page`
- Returns: An object containing a paginated list of questions belonging to the specified category, and the total number of questions in this category
```
{
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    ...
  ], 
  "total_questions": 3
}
```

#### GET /questions
- Fetch all questions
- Request arguments:
    - Query parameters: `page`
- Returns: An object containing a paginated list of questions, the total number questions, and an object containing all the categories
```
{
  "categories": {
    "1": "Science", 
    "2": "Art",
    ...
  }, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    ...
  ], 
  "total_questions": 19
}
```

#### POST /questions
- Add a new question
- Request arguments:
    - JSON body:
        >{"question": "Will this work?",\
        >"answer": "Maybe",\
        >"difficulty": 1,\
        >"category": 1}
- Returns: An object indicating the success of the request, and the ID of the newly created question

#### DELETE /questions/<question_id>
- Delete a question by its ID
- Request arguments: None
- Returns: An object indicating the success of the request

#### POST /questions/search
- Fetch questions matching a search term
- Request arguments:
    - Query parameters: `page`
    - JSON body:
        >{"search_term": "title"}
- Returns: An object containing a paginated list of questions matching the search term, and the total number of matching questions

#### POST /quizzes
- Fetch a random question belonging to the quiz category (if provided) that is not one of the previous questions
- Request arguments:
    - JSON body:
        >{"previous_questions": [16, 17],\
        >"quiz_category": 2}
- Returns: An object containing a single question

## Testing

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```