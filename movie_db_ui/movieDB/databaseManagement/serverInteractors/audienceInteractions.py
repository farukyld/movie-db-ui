from . import databaseConnection as __cnx

def buyTicket(username, sessionId):
    cursor = __cnx.cursor()
    try:
        query = "INSERT INTO BoughtTicket(audienceUserName, sessionId) VALUES('{}', {});"
        query= query.format('faruu', 50001)
        cursor.execute(query )
        __cnx.commit()
        return True, "Ticket for session {} bought successfully".format(sessionId)
    except Exception as e:
        __cnx.rollback()
        raise e

def rate(username, movieId, points):
    cursor = __cnx.cursor()
    try:
        query = """
        INSERT INTO Rating(audienceUserName, movieId, points)
        VALUES('{}',{},{});
        """
        query.format(username, movieId, points)
        cursor.execute(query)
        __cnx.commit()
        return True
    except Exception as e:
        __cnx.rollback()
        raise e


def listSessions():
    cursor = __cnx.cursor()
    try:
        # fetch all session data
        query = """
        SELECT 
            ms.sessionId,
            m.movieId, 
            m.movieName, 
            d.surname AS directorSurname,
            rp.platformName,
            ms.theatreId, 
            ms.timeSlot
        FROM Directors d
            JOIN Movies m ON d.username = m.directorUserName
            JOIN RatingPlatform rp ON d.platformId = rp.platformId
            JOIN MovieSessions ms ON m.movieId = ms.movieId
        """
        cursor.execute(query)

        fetchResult = cursor.fetchall()
        headers = [i[0] for i in cursor.description]

        # fetch predecessors for each movie and 
        # append to the associated fetch result entry
        returnResult=[]
        for row in fetchResult:
            movieId = row[0]
            query = """
            SELECT 
                p.predecessorMovieId
            FROM Precedes p
            WHERE p.successorMovieId = {};
            """
            cursor.execute(query.format(movieId))
            predecessors = cursor.fetchall()
            predecessors_str = ', '.join(str(i[0]) for i in predecessors)
            returnResult.append(row + (predecessors_str,))

        headers.append('predecessorList')

        return True, headers, returnResult

    except Exception as e:
        __cnx.rollback()
        raise e

def listBoughtTickets(audienceUsername):
    cursor = __cnx.cursor()
    try:
        query = """
        SELECT 
            m.movieId, 
            m.movieName, 
            bt.sessionId,
            r.points AS Rating,
            (SELECT COUNT(*) FROM Rating WHERE movieId = m.movieId) AS RatingCount,
            m.averageRating AS OverallRating
        FROM BoughtTicket bt
        JOIN MovieSessions ms ON bt.sessionId = ms.sessionId
        JOIN Movies m ON ms.movieId = m.movieId
        LEFT JOIN Rating r ON m.movieId = r.movieId AND r.audienceUserName = '{}'
        WHERE bt.audienceUserName = '{}';
        """
        cursor.execute(query.format(audienceUsername, audienceUsername))
        result = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        return True, headers, result
    except Exception as e:
        __cnx.rollback()
        raise e


def previewTicket(sessionId):
    cursor = __cnx.cursor()
    try:
        query = "SELECT m.movieId, m.movieName, ms.sessionId, r.points AS Rating, (SELECT COUNT(*) FROM Rating WHERE movieId = m.movieId) AS RatingCount, m.averageRating AS OverallRating FROM MovieSessions ms JOIN Movies m ON ms.movieId = m.movieId LEFT JOIN Rating r ON m.movieId = r.movieId WHERE ms.sessionId = {};"
        cursor.execute(query.format(sessionId))
        result = cursor.fetchall()
        headers = [i[0] for i in cursor.description]
        return True, headers, result
    except Exception as e:
        __cnx.rollback()
        raise e
