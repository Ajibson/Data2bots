# Data2bots

## Main Technologies Used
1. Django (code development)
2. Django Rest Framework (API development)
3. Black (formatting)
4. Flake8 (code quality check)
5. Git (Version Control)
6. Sqlite3 (Database)
7. Swagger (documentation)

## Install dependencies
pip install -r requirements.txt

## Run the tests
coverage run manage.py test

### See coverage report
coverage report (99% coverage)

## Start the application
First ensure you are at the directory with the manage.py file, then run
#### python manage.py runserver

## Visit the docs
http://127.0.0.1:8000/docs/

## Visit the admin page
http://127.0.0.1:8000/admin/

## Database Schema Used
https://drawsql.app/teams/report/diagrams/data2bots

## Notes
1. Admin user exist with the credential: *email: admin@mail.com password: admin123*
2. Some dummy products are already created 
3. Some dummy payments also already exists
4. some dummy order history also exist
