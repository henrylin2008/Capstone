Capstone: Casting Agency App
----
## Introduction
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

* Roles:
    * Casting Assistant
        * Can view actors and movies
    * Casting Director
        * All permissions a Casting Assistant has and…
        * Add or delete an actor from the database
        * Modify actors or movies
    * Executive Producer
        * All permissions a Casting Director has and…
        * Add or delete a movie from the database

## Getting Started

## Tech Stack 

### Backend

### Frontend

## Initial setup

## Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

## Project Steps
##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql 
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

## API Reference
Getting Started
- Backend Base URL: http://127.0.0.1:5000/
- Frontend Base URL: http://localhost:3000

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

### Endpoints 

#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
- Sample: curl http://127.0.0.1:5000/categories
```

```

#### GET '/questions'
- Fetches a list of question objects, total number of questions, and the category that question belongs to
- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1
- Sample: curl http://127.0.0.1:5000/questions

```

```


#### DELETE /questions/{question_id}
- Deleting a question matched with designated question ID of it exists. 
- Returns the id of the deleted question, current questions on the page,  success value, and total questions. 
- Sample: curl -X DELETE http://127.0.0.1:5000/questions/21

```

```

#### POST /questions
- Creates a new question with the question, answer, difficulty, and category. 
- If question or answer fields are left as blank, then return 422 
- Returns the id of the question, current category, success value, and total questions
- Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d 
  '{"question":"new question", "answer":"answer", "difficulty":"1", "category":"6"}'
```

```


#### GET /categories/{category_id}/questions
- This endpoint GET questions based on the category. It should return current category, questions in this category, 
  success value, and total questions
- Returns success value, and total number of questions 
- Sample: curl 127.0.0.1:5000/categories/1/questions
```

```

#### POST /quizzes
- Getting questions to play the quiz. This endpoint should take category and previous question parameters and return
  a random questions within the given category, if provided, and that is not one of the previous questions.
- Returns: multiple key/value pairs object with the following content: 
    * success: True or False 
    * question: random question from the list of available questions in the category/categories, which it contains
                details about the question: answer, category, difficulty, id, and question content
```

```

### Error Handling
```
Errors are returned as JSON objects in the following format:
{   
    "success": False, 
    "error": 422, 
    "message": "Unprocessable"
}
```
The API will return five error types when requests fail: 
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Server Error