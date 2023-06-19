CREATE TABLE DBManager (
    username CHAR(50),
    userPassword CHAR(50) NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE Audience (
    username CHAR(50),
    userPassword CHAR(50) NOT NULL,
    firstName CHAR(50) NOT NULL,
    surname CHAR(50) NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE RatingPlatform (
    platformId INTEGER AUTO_INCREMENT,
    platformName CHAR(50) NOT NULL,
    PRIMARY KEY (platformId),
    UNIQUE (platformName)
) AUTO_INCREMENT = 10130;

CREATE TABLE Directors (
    username CHAR(50),
    userPassword CHAR(50) NOT NULL,
    firstName CHAR(50) NOT NULL,
    surname CHAR(50) NOT NULL,
    nation CHAR(50) NOT NULL,
    platformId INTEGER,
    PRIMARY KEY (username),
    FOREIGN KEY (platformId) REFERENCES RatingPlatform (platformId)
     ON DELETE SET NULL
     -- maybe I can raise a trigger with a message saying 
     -- those directors are now platformless.
);

CREATE TABLE Genre (
    genreId INTEGER AUTO_INCREMENT,
    genreName CHAR(50) NOT NULL,
    PRIMARY KEY (genreId),
    UNIQUE (genreName)
)AUTO_INCREMENT = 80001;

CREATE TABLE Theatres (
    theatreId INTEGER AUTO_INCREMENT,
    theatreName CHAR(50) NOT NULL,
    theatreCapacity INTEGER NOT NULL,
    theatreDistrict CHAR(50) NOT NULL,
    PRIMARY KEY (theatreId)
)AUTO_INCREMENT = 40001;



CREATE TABLE Movies (
    movieId INTEGER AUTO_INCREMENT,
    movieName CHAR(50) NOT NULL,
    duration INTEGER NOT NULL,
    averageRating DECIMAL,
    directorUserName CHAR(50) NOT NULL,
    PRIMARY KEY (movieId),
    FOREIGN KEY (directorUserName) REFERENCES Directors (username)
     ON DELETE NO ACTION
     -- I think deleting the movie directly when a director leaves \
     -- will be so harsh to audience that already bought ticket for this movie.
     -- so, someone wanting to remove a director, should think other way around.
     -- we don't remove them anyways.
)AUTO_INCREMENT = 20001;

CREATE TABLE MovieSessions (
    sessionId INTEGER AUTO_INCREMENT,
    showDate DATE NOT NULL,
    timeSlot INTEGER NOT NULL,
    theatreId INTEGER NOT NULL,
    movieId INTEGER NOT NULL,
    PRIMARY KEY (sessionId),
    FOREIGN KEY (theatreId) REFERENCES Theatres (theatreId) 
     ON DELETE CASCADE,
    FOREIGN KEY (movieId) REFERENCES Movies (movieId)
     ON DELETE CASCADE
     -- we can simply delete the session if movie or the Theatre is deleted \
     -- because nothing depends on session
)AUTO_INCREMENT = 50001;

CREATE TABLE SubscribedTo (
    audienceUserName CHAR(50),
    platformId INTEGER,
    PRIMARY KEY (audienceUserName, platformId), 
    -- many to many reln. so use both forn keys as pkey \
    -- to allow multiple existence of an audience or a platform.
    FOREIGN KEY (audienceUserName) REFERENCES Audience (username)
     ON DELETE CASCADE,
    FOREIGN KEY (platformId) REFERENCES RatingPlatform (platformId)
     ON DELETE CASCADE
     -- we can delete subscription info when some of the forn keys is deleted,\
     -- because nothing depend on it.
);

CREATE TABLE BoughtTicket (
    audienceUserName CHAR(50),
    sessionId INTEGER,
    PRIMARY KEY (audienceUserName, sessionId),
    FOREIGN KEY (audienceUserName) REFERENCES Audience (username)
     ON DELETE CASCADE,
    FOREIGN KEY (sessionId) REFERENCES MovieSessions (sessionId)
     ON DELETE CASCADE
     -- similarly, delete ticketBought info if audience or session is removed.
);

CREATE TABLE Rating (
    audienceUserName CHAR(50),
    movieId INTEGER,
    points DECIMAL,
    PRIMARY KEY (audienceUserName, movieId),
    FOREIGN KEY (audienceUserName) REFERENCES Audience (username)
     ON DELETE CASCADE,
    FOREIGN KEY (movieId) REFERENCES Movies (movieId)
     ON DELETE CASCADE
     -- we may need to update the average rating of the movie. 
     -- but I am not able to represent that here.
);

CREATE TABLE CategorizedBy (
    movieId INTEGER,
    genreId INTEGER,
    PRIMARY KEY (movieId, genreId),
    FOREIGN KEY (movieId) REFERENCES Movies (movieId)
     ON DELETE CASCADE,
    FOREIGN KEY (genreId) REFERENCES Genre (genreId)
     ON DELETE CASCADE
     -- if one of those forn. keys are deleted, 
     -- we no more need to store the reln. among them. 
);

CREATE TABLE Precedes (
    predecessorMovieId INTEGER,
    successorMovieId INTEGER,
    PRIMARY KEY (predecessorMovieId, successorMovieId),
    FOREIGN KEY (predecessorMovieId) REFERENCES Movies (movieId)
     ON DELETE CASCADE,
    FOREIGN KEY (successorMovieId) REFERENCES Movies (movieId)
     ON DELETE CASCADE
);
