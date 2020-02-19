# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

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

## API Endpoints

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

GET '/questions'
- Retrieves a paginated list of questions that can be played in the trivia game
- Request Parameters: page:integer
- Returns: An object that contains the categories, currently selected category, list of questions and the total count of questions
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    .
    .
    .
  ],
  "success": true,
  "total_questions": 22
}
```

DELETE '/questions/{id}'
- Deletes a question by a given id
- Returns: An object containing the id of the successfully deleted question and the updated count of questions
```
{
    "success": True,
    "deleted_id": 28,
    "total_questions": 27
}
```

POST '/questions'
- Adds a new question to be played in the trivia game
- Request Body Arguments:
    - question(string): the question to be displayed on the game.
    - answer(string): the correct answer for the question.
    - difficulty(integer): rating on how difficult the question is.
    - category(integer): the id of the category where the question belongs
- Returns: An object that contains the id of the new question inserted and updated count of questions

```
#sample request body
{
    'question' : "Will this test pass?",
    'answer': "Yes, Definitely!",
    'difficulty': 1,
    'category': 1
}
```

```
#sample response
{
    "success": True,
    "created": 28,
    "total_questions": 28
}

```

POST '/questions'
- Retrieves a list of questions that contains the search term 
- Request Body Arguments:
    - searchTerm(string): search term to mathc the questions
- Returns: An object containing the matching questions, count of found questions and currently selected category

```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

GET '/categries/{category_id}/questions'
- Retrieves the questions under the selected category
- Returns: An object containing the list of questions, count of matching questions and the current category

```
{
  "current_category": "Entertainment",
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

POST '/quizzes'
- Retrieves a question under a selected category (if any) and that is not previously asked
- Request Body Arguments:
    - previous_questions([int]):  a list of ids of the questions that were previously asked
    - category({category}): a category object
- Returns: a question object

```
#sample request
{
    "previous_questions": [20,22],
    "category": {
        "id": 1
        "type": "Science"
    }
}
```

```
#sample response
{
    "success": True,
    "question": {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    }
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```