from . import databaseConnection as __cnx



__CRED_QUERY = "SELECT * FROM {} WHERE username='{}' AND userPassword='{}'"

def checkCredDirector(username:str, password:str):
    cursor = __cnx.cursor()
    cursor.execute(__CRED_QUERY.format('directors', username, password))
    result = cursor.fetchone()
    cursor.close()
    return result is not None

def checkCredAudience(username, password):
    cursor = __cnx.cursor()
    cursor.execute(__CRED_QUERY.format('Audience', username, password))
    result = cursor.fetchone()
    cursor.close()
    return result is not None

def checkCredDB_manager(username, password):
    cursor = __cnx.cursor()
    cursor.execute(__CRED_QUERY.format('dbmanager', username, password))
    result = cursor.fetchone()
    cursor.close()
    return result is not None
