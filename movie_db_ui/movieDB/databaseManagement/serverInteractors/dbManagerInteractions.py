from . import databaseConnection as __cnx


def addAudience( name, surname, userName, userPassword):
    cursor = __cnx.cursor()
    try:
        query = """
        INSERT INTO audience (firstName, surname, userName, userPassword) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, surname, userName, userPassword))
        __cnx.commit()
    except Exception as e:
        __cnx.rollback()
        raise e
    cursor.close()
    return True, "Audience added successfully"


def addDirector( username:str, userPassword:str, firstName:str, surname:str, nation:str, ratingPlatformId:int):
    cursor = __cnx.cursor()
    try:
        query = """
        INSERT INTO directors (username, userPassword, firstName, surname, nation, platformId) 
        VALUES ('{}', '{}', '{}', '{}', '{}', {});
        """
        query = query.format(username, userPassword, firstName, surname, nation, ratingPlatformId if ratingPlatformId else 'NULL')
        cursor.execute(query)
        __cnx.commit()
    except Exception as e:
        __cnx.rollback()
        raise e
    cursor.close()
    return True, "Director added successfully"


def deleteAudience(username):
    cursor = __cnx.cursor()
    
    cursor.execute("SELECT * FROM audience WHERE username = '{}'".format(username))
    fetchResult = cursor.fetchall()
    if not fetchResult:
        return False, "there is no user with username: {}".format(username)
    
    try:
        query = "DELETE FROM audience WHERE username = '{}'"
        query = query.format(username)
        cursor.execute(query)
        __cnx.commit()
    except Exception as e:
        __cnx.rollback()
        raise e
    cursor.close()
    return True,"Audience {} deleted successfully".format(username)


def addPlatform(platformName:str):
    cursor = __cnx.cursor()
    try:
        query = "INSERT INTO ratingPlatform ( platformName) VALUES ( '{}');"
        query = query.format(platformName)
        cursor.execute(query)
        __cnx.commit()
    except Exception as e:
        __cnx.rollback()
        raise e
    cursor.close()
    return True, "Platform added successfully"


def updateDirectorPlatform(username, platform_id):
    cursor = __cnx.cursor()

    cursor.execute("SELECT * FROM directors WHERE username = '{}'".format(username))
    fetchResult = cursor.fetchall()
    if not fetchResult:
        return False, "there is no director with username: {}".format(username)
    

    try:
        query = """
        UPDATE directors
        SET platformId = {}
        WHERE username = '{}'
        """
        query = query.format(platform_id if platform_id else 'NULL', username)
        cursor.execute(query)
        __cnx.commit()
    except Exception as e:
        __cnx.rollback()
        raise e
    cursor.close()
    return True, "Director's platform updated successfully"


def listDirectors():
    cursor = __cnx.cursor()
    try:
        query = "SELECT * FROM Directors"
        cursor.execute(query)
        result = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        return True, headers, result
    except Exception as e:
        __cnx.rollback()
        raise e

def listPlatforms():
    cursor = __cnx.cursor()
    try:
        query = "SELECT * FROM RatingPlatform"
        cursor.execute(query)
        result = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        return True, headers, result
    except Exception as e:
        __cnx.rollback()
        raise e

def listAudience():
    cursor = __cnx.cursor()
    try:
        query = "SELECT * FROM Audience"
        cursor.execute(query)
        result = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        return True, headers, result
    except Exception as e:
        __cnx.rollback()
        raise e

def listRatings_ofAudience(username):
    cursor = __cnx.cursor()
    try:
        query = """
        SELECT 
            m.movieId, 
            m.movieName, 
            r.points
        FROM Rating r
            JOIN Movies m ON m.movieId = r.movieId
        WHERE r.audienceUserName = '{}';
        """
        query = query.format(username)
        cursor.execute(query)
        result = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        return True, headers, result
    except Exception as e:
        __cnx.rollback()
        raise e

def listSessions_ofDirector(username):
    cursor = __cnx.cursor()
    try:
        query = """
        SELECT 
            m.movieId, 
            m.movieName, 
            t.theatreId, 
            t.theatreDistrict, 
            s.showDate, 
            s.timeSlot
        FROM Directors d
            JOIN Movies m ON m.directorUserName = d.username
            JOIN MovieSessions s ON s.movieId = m.movieId
            JOIN Theatres t ON t.theatreId = s.theatreId
        WHERE d.username = '{}';
        """
        query = query.format(username)
        cursor.execute(query)
        result = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        return True, headers, result
    except Exception as e:
        __cnx.rollback()
        raise e



def viewOverallRating(movieId):
    cursor = __cnx.cursor()
    try:
        # using left join here, ensures if no rating exists for a movie,
        # resulting set contains one movie with associated rating data is null.
        query = """
        SELECT 
            m.movieId,
            m.movieName, 
            COUNT(r.audienceUserName) AS NumberOfRatings, 
            COALESCE(AVG(r.points), 0) AS AverageRating
        FROM Movies m
            LEFT JOIN Rating r ON m.movieId = r.movieId
        GROUP BY 
            m.movieId,
            m.movieName;
        HAVING m.movieId = {}
        """
        query = query.format(movieId)
        cursor.execute(query)
        result = cursor.fetchall()

        headers = [i[0] for i in cursor.description]
        
        return True, headers, result
    except Exception as e:
        __cnx.rollback()
        raise e
