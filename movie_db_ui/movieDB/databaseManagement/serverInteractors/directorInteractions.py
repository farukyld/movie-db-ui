from . import databaseConnection as __cnx
from . import _extractQueries
def addPredecessor(predecessorId, successorId):
    cursor = __cnx.cursor()
    try:
        query = "INSERT INTO precedes (predecessorMovieId, successorMovieId) VALUES ({}, {})"
        query = query.format(predecessorId, successorId)
        cursor.execute(query)
        __cnx.commit()
        cursor.close()
        return True, "Predecessor added successfully."
    except Exception as e:
        __cnx.rollback()
        raise e

def addMovie(directorUsername, movieName, duration, genres):
    cursor = __cnx.cursor()
    try:
        query0 = "SELECT movieName FROM Movies WHERE movieName = '{}'"
        query0 = query0.format(movieName)
        cursor.execute(query0)
        if cursor.fetchone() is not None:
            return False, "A movie with that name already exists."
        query1 = "INSERT INTO Movies (directorUserName, movieName, duration) VALUES ('{}', '{}', {})"
        query1 = query1.format(directorUsername, movieName, duration)
        # insert movie
        cursor.execute(query1)
        addedMovieId = cursor.lastrowid
        validGenres = []
        invalidGenres = []
        for genre in genres:
            query2 = "SELECT genreId FROM Genre WHERE genreName = '{}'"
            formattedQuery = query2.format(genre)
            cursor.execute(formattedQuery)
            fetchResult = cursor.fetchall()
            if fetchResult:
                # insert genres
                query3 = "INSERT INTO categorizedBy (movieId, genreId) VALUES ({}, {})"
                query3 = query3.format(addedMovieId, fetchResult[0][0])
                cursor.execute(query3)
                validGenres.append(genre)
            else:
                invalidGenres.append(genre)
        if not validGenres:
            __cnx.rollback() # if no genre relation inserted, remove movie.
            cursor.execute("select genreName from genre")
            
            return False, "None of the genres provided exists. try one of the following: {}".format(
                ", ".join(i[0] for i in cursor.fetchall())
            )
        __cnx.commit()
        message = "Movie {} added successfully with genres: {}.".format(movieName, ", ".join(validGenres))
        if invalidGenres:
            message += "Warning!! those genres were not in database: {}".format(", ".join(invalidGenres))
        return True, message
    except Exception as e:
        __cnx.rollback()
        raise e

def addTheatre(directorUsername, theatreName, theatreDistrict, theatreCapacity):
    cursor = __cnx.cursor()
    try:
        query = "SELECT theatreName FROM Theatres WHERE theatreName = '{}'"
        query = query.format(theatreName)
        cursor.execute(query)
        if cursor.fetchone() is not None:
            return False, "A theatre with that name already exists."
        query = "INSERT INTO Theatres (theatreName, theatreDistrict, theatreCapacity) VALUES ('{}', '{}', {})"
        query = query.format(theatreName, theatreDistrict, theatreCapacity, directorUsername)
        cursor.execute(query)
        __cnx.commit()
        return True, "Theatre {} added successfully.".format(theatreName)
    except Exception as e:
        __cnx.rollback()
        raise e

def __movieBelongsDirector(directorUsername, movieId):
    cursor = __cnx.cursor()
    query = "SELECT directorUserName FROM Movies WHERE movieId = {}"
    query = query.format(movieId)
    cursor.execute(query)
    result = cursor.fetchone()
    return result and result[0] == directorUsername
    
def addSession(directorUsername, movieId, theatreId, timeslot, date):
    cursor = __cnx.cursor()
    try:
        # check if that movie belongs to the director
        if not __movieBelongsDirector(directorUsername, movieId):
            return False, "this movie with id {} doesn't belongs to you".format(movieId)
        query = "INSERT INTO MovieSessions (movieId, theatreId, timeslot, showDate) VALUES ({}, {}, {}, '{}')"
        query = query.format(movieId, theatreId, timeslot, date.strftime('%Y-%m-%d'))
        cursor.execute(query)
        __cnx.commit()
        return True, "Session added successfully."
    except Exception as e:
        __cnx.rollback()
        raise e

def updateMovieName(directorUsername, movieId, movieName):
    cursor = __cnx.cursor()
    try:
        # check if the movie belongs to the director
        if not __movieBelongsDirector(directorUsername, movieId):
            return False, "this movie with id {} doesn't belongs to you".format(movieId)
        # update the movie name
        query = "UPDATE Movies SET movieName = '{}' WHERE movieId = {}"
        query = query.format(movieName, movieId)
        cursor.execute(query)
        __cnx.commit()
        return True, "Movie name updated successfully."
    except Exception as e:
        __cnx.rollback()
        raise e

def getSessionlessMovies(username):
    cursor = __cnx.cursor()
    try:
        query = "SELECT m.* FROM Movies m LEFT JOIN MovieSessions ms ON m.movieId = ms.movieId WHERE ms.sessionId IS NULL;"
        cursor.execute(query)
        result = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        return True, headers, result
    except Exception as e:
        __cnx.rollback()
        raise e

def getMovieAudience(username, movieId):
    cursor = __cnx.cursor()
    try:
        if not __movieBelongsDirector(username, movieId):
            return False, "this movie with id {} doesn't belongs to you".format(movieId)
        
        query = "SELECT a.username, a.firstName, a.surname FROM Audience a JOIN BoughtTicket bt ON a.username = bt.audienceUserName JOIN MovieSessions ms ON bt.sessionId = ms.sessionId WHERE ms.movieId = '{}';"
        query = query.format(movieId)
        cursor.execute(query)
        result = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        return True, headers, result
    except Exception as e:
        __cnx.rollback()
        raise e

def getSessionsMovies(directorUserName):
    cursor = __cnx.cursor()
    try:
        # first fetch the sessions
        query = "SELECT m.movieId, m.movieName, ms.theatreId, ms.showDate, ms.timeSlot FROM Directors d JOIN Movies m ON d.username = m.directorUserName JOIN MovieSessions ms ON m.movieId = ms.movieId WHERE d.username = '{}' ORDER BY m.movieId ASC;"
        query = query.format(directorUserName)
        cursor.execute(query)

        fetchResult = cursor.fetchall()
        headers = [i[0] for i in cursor.description]

        # then fetch and append the predecessors for each movie.
        returnResult=[]
        for row in fetchResult:
            movieId = row[0]
            query = "SELECT p.predecessorMovieId FROM Precedes p WHERE p.successorMovieId = {};"
            query = query.format(movieId)
            cursor.execute(query)
            predecessors = cursor.fetchall()
            predecessors_str = ', '.join(str(i[0]) for i in predecessors)
            # Append the string of predecessor movieIds to this row
            returnResult.append(row + (predecessors_str,))

        headers.append('predecessorList')

        return True, headers, returnResult

    except Exception as e:
        __cnx.rollback()
        raise e

def listAvailableTheatres(username, date, slot, duration):
    cursor = __cnx.cursor()
    try:
        ## take duration into account
        query = """
        SET @tarih = {};
        SET @slot = {};
        SET @duration = {};

        WITH sessIntervals as (
            SELECT  
                ms.showDate as sessDate, 
                ms.timeSlot as startTime, 
                ms.timeSlot + m.duration as endTime,
                ms.theatreId

            FROM moviesessions as ms
            INNER JOIN movies as m on m.movieId =ms.movieId
            WHERE showDate = @tarih
        )

        SELECT t.theatreId, t.theatreDistrict, t.theatreCapacity

        FROM theatres as t

        WHERE @slot + @duration < 4

        AND not EXISTS (
            SELECT *
            FROM sessIntervals as ssin1
            WHERE t.theatreId = ssin1.theatreId and (
            (ssin1.startTime < @slot + @duration and ssin1.startTime > @slot)
            or (ssin1.endTime > @slot and ssin1.endTime < @slot + @duration)) 
            
            )
        """

        query = query.format(date.strftime('%Y-%m-%d'), slot, duration)
        queries = _extractQueries(query,";")

        for query in queries:
            cursor.execute(query)
            result= cursor.fetchall()

        headers = [i[0] for i in cursor.description]
        __cnx.commit()

        return True, headers, result
    except Exception as e:
        __cnx.rollback()
        raise e
