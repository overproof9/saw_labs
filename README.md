# saw_labs
set up

create .env file in folder bitter/

    SECRET_KEY=<secret>

    DB_STRING=<connection string>


run project

    python3 -m pip install -r requirements.txt

    cd lab1\bitter

    flask db init

    flask db migrate -m 'Initial migration'

    flask db upgrade

    flask run
