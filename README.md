# movie-db-ui

## purpose
this project aims to practice front-end, back-end, database communication using python-django and mysql. We didn't use django's orm in this project in order to have a deeper understanding of how back-ends interact with databases. 

## what it does 
this is an application that enables different user types (database managers, directors, audience) to interact with a database called movie database via a UI. 

## how to run
within the `movie_db_ui` directory
for linux execute
```bash
# install the required python packages
python -m pip install -r requirements.txt
# export those variables according to your mysql server connection
# I assumed here, user has the privileges 
# to SELECT, INSERT, UPDATE, DELETE, CREATE, REFERENCES, INDEX, EXECUTE on the database.
export $p3_Database=""
export $p3_User=""
export $p3_userPass=""
export $p3_Host=""
export $p3_Port=""
# then run the server
python manage.py runserver
# in order to create the database tables and insert some initial records,
# you should run this script:
python initiate_databse.py
```
for windows execute this in powershell
```powershell
# install the required python packages
python -m pip install -r requirements.txt

# export those variables according to your mysql server connection
# I assumed here, user has the privileges 
# to SELECT, INSERT, UPDATE, DELETE, CREATE, REFERENCES, INDEX, EXECUTE on the database.
$env:p3_Database = ""
$env:p3_User = ""
$env:p3_userPass = ""
$env:p3_Host = ""
$env:p3_Port = ""

# then run the server
python manage.py runserver

# in order to create the database tables and insert some initial records,
# you should run this script:
python initiate_databse.py

```

then connect the UI via your browser by [http://127.0.0.1:8000](http://127.0.0.1:8000)

you can check out the initial records inside [insertInitials.sql](\movie_db_ui\movieDB\databaseManagement\sqlFiles\insertQueries\insertInitials.sql)

you can log in as a database manager and create directors, audience etc. detailed information is in the [project description](https://github.com/farukyld/movie-db-ui/wiki/Project-Description)
