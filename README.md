# movie-db-ui
this is an application that enables different user types (database managers, directors, audience) to interact with a database called movie database via a UI. 

## how to run
within the `code\movie_db_ui` directory
execute
```bash
# install the required python packages
python -m pip install -r requirements.txt
# export those variables according to your mysql server connection
# I assumed here, user has the privileges 
# to SELECT, INSERT, UPDATE, DELETE, CREATE, REFERENCES, INDEX, EXECUTE on the database.
export $p3_Database=
export $p3_User=
export $p3_userPass=
export $p3_Host=
export $p3_Port=
# then run the server
python manage.py runserver
# in order to create the database tables and insert some initial records,
# you should run this script:
python initiateServer.py
```
then connect the UI via your browser by 127.0.0.1
you can check out the initial records inside this (file)[code\movie_db_ui\movieDB\databaseManagement\sqlFiles\insertQueries\insertInitials.sql]
you can log in as a database manager and create directors, audience etc. detailed information is in the (project description)[]
