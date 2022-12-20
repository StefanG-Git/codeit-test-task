## What Is This?

Implementation of the task from CodeIT.

Simple CRM system for companies app created using Django Rest Framework and postgresql db.

 - CRUD API to manage companies

 - CRUD API to manage company employees

## Installation

#### Clone the repository

`https://github.com/StefanG-Git/codeit-test-task.git`

#### Create virtual environment 

`python -m venv venv`

####  Activate virtual environment

`.\venv\Scripts\activate`

####  Install all the dependencies

`pip install -r requirements.txt`

#### Set up environment variables in `.env` file

```
SECRET_KEY=
DEBUG=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
```

#### Apply migrations

`python manage.py migrate`

#### Start the project

`python manage.py runserver`

## Structure

`Company API`

| Endpoint           | Method | Result                 |
|--------------------|--------|------------------------|
| `/companies`       | GET    | List all companies     |
| `/companies`       | POST   | Create a new company   |
| `/companies/{id}/` | GET    | Get a company `:id`    |
| `/companies/{id}/` | PUT    | Update a company `:id` |
| `/companies/{id}/` | DELETE | Delete a company `:id` |



`Employee API`

| Endpoint           | Method | Result                  |
|--------------------|--------|-------------------------|
| `/employees`       | GET    | List all employees      |
| `/employees`       | POST   | Create a new employee   |
| `/employees/{id}/` | GET    | Get a employee `:id`    |
| `/employees/{id}/` | PUT    | Update a employee `:id` |
| `/employees/{id}/` | DELETE | Delete a employee `:id` |

