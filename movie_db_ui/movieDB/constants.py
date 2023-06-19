from enum import Enum as __Enum



class UserTypes(__Enum):
    DIRECTOR = ("Director", "Director")
    DB_MANAGER = ("DB_Manager", "DB Manager")
    AUDIENCE = ("Audience", "Audience")

    def __init__(self, value, displayName):
        self._value_ = value
        self.displayName = displayName


USER_TYPES = [(user.value, user.displayName) for user in UserTypes]


class DBM_ListingOperation(__Enum):
    DIRECTORS = ("directors", "List Directors")
    PLATFORMS = ("platforms", "List Platforms")
    AUDIENCE = ("audience", "List Audience")
    AUDIENCE_RATINGS = ("audienceRatings", "List Ratings of Audience")
    DIRECTOR_SESSIONS = ("directorSessions", "List Sessions of Director")
    MOVIE_OVERALL_RATING = ("movieOverallRating", "View Overall Rating of a Movie")

    def __init__(self, value, displayName):
        self._value_ = value
        self.displayName = displayName

DBM_LISTING_OPERATIONS = [(operation.value, operation.displayName) for operation in DBM_ListingOperation]


class DrtListingOperations(__Enum):
    SLOT_AVAILABLE_THETRS = ("slotsAvailableTheatres", "List Available Theatres for Date/Slot")
    SESSIONS_MOVIES = ("sessions_andMovies", "List registered session/movie info")
    MOVIE_AUDIENCE = ("audience_ofMovie", "List audience that bought ticket for a movie")
    SESSIONLESS_MOVIES = ("movies_woSession", "List movies that haven't allocated session yet") 
    
    def __init__(self, value, displayName):
        self._value_ = value
        self.displayName = displayName

DRT_LISTING_OPERATIONS = [(operation.value, operation.displayName) for operation in DrtListingOperations]



class AudListingOperations(__Enum):
    SESSIONS = ("allSessions", "List all sessions info")
    BOUGHT_TICKETS = ("boughtTickets", "List all bought tickets info")
    
    def __init__(self, value, displayName):
        self._value_ = value
        self.displayName = displayName

AUD_LISTING_OPERATIONS = [(operation.value, operation.displayName) for operation in AudListingOperations]
