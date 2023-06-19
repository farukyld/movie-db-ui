from . import databaseConnection as __cnx, _listFileNamesByRelativePath as __listFileNamesByRelativePath
from . import _extractQueries as __extractQueries

from glob import glob as __glob
from mysql.connector import IntegrityError as __IntegrityError





def createTables():
    cursor = __cnx.cursor()
    
    cursor.execute("show tables")
    tables = cursor.fetchall()
    __cnx.commit()
    if tables:
        return False, "tables already created"
    # here I assume all tables are created at one shot,
    # in order to make this code simpler.
    
    # also note that, in mysql, data definition language
    # is not tansactional. meaning they cant be rolled back
    # even if I try to roll table creation back
    #  when an error occured in this function, it won't do anything.

    fileNames = __listFileNamesByRelativePath(__file__,'../sqlFiles/createTableQueries/','*.sql')

    for fileName in fileNames:
        with open(fileName) as sql_file:
            sqlScript = sql_file.read()
        
        queries = __extractQueries(sqlScript,";")

        for query in queries:
            cursor.execute(query)
            cursor.fetchall()
            __cnx.commit()
    
    cursor.close()
    return True, fileNames


def insertInitialRecords():
    cursor = __cnx.cursor()
    
    cursor.execute("show tables")
    tables = cursor.fetchall()
    __cnx.commit()
    if not tables:
        return False, "there is no table"

    fileNames = __listFileNamesByRelativePath(__file__,'../sqlFiles/insertQueries/','insertInitials.sql')

    try:
        for fileName in fileNames:
            with open(fileName) as sql_file:
                sqlScript = sql_file.read()
            
            queries = __extractQueries(sqlScript,";")
            
            for query in queries:
                cursor.execute(query)
                cursor.fetchall()
                __cnx.commit()
    except __IntegrityError as err:
        return False, err
    
    cursor.close()
    return True, fileNames
    

