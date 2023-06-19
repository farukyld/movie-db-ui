from mysql.connector import connect as __connect
from glob import glob as __glob
from os.path import join as __join, dirname as __dirname, normpath as __normpath
from movie_db_ui.settings import DATABASES as __DATABASES

databaseConnection = __connect(
    host=__DATABASES['default']['HOST'],
    user=__DATABASES['default']['USER'],
    password=__DATABASES['default']['PASSWORD'],
    database=__DATABASES['default']['NAME'],
)

databaseConnection.autocommit=False



def _listFileNamesByRelativePath(currentPythonFile,relativePath,wildchard):
    """
    Lists file names by relative path.

    Args:
        currentPythonFile (str): __file__ global vaiable of the caller.
        relativePath (str): The relative path to the target folder.
        wildchard (str): The wildcard pattern to match the files.

    Returns:
        list: A list of file names matching the wildcard pattern.
    """
    folderPath = __join(__dirname(__file__), relativePath)
    fileNames = [__normpath(filename) for filename in __glob(__join(folderPath, wildchard))]
    return fileNames

def fn():
    pass

def _extractQueries(sqlScript:str, delims:str):
    queries = [query.strip() for query in sqlScript.split(delims)] 
    queries = [query for query in queries if query]
    return queries

