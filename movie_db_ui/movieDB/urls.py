from django.urls import path
from .views import commonViews, dbmViews, drtViews, audViews
urlpatterns = [
    path('',commonViews.index,name='index'),

    # those two are commented out for now. 
    # later I will add a small authentication mechanism for them
    # path('createDatabaseTables#',commonViews.createTables,          name='createTables'),
    # path('insertInitialRecords#',commonViews.insertInitialRecords,  name='insertInitialRecords'),

    path('loginIndex/<str:message>/',   commonViews.loginIndex, name='loginIndex_'),
    path('loginIndex/',                 commonViews.loginIndex, name='loginIndex'),
    path('login/',                      commonViews.login,      name='login'),

    path('dbManagerHome/',                              dbmViews.dbManagerHome,                     name='dbManagerHome'),
    path('dbManagerHome/addAudience/',                  dbmViews.dbManagerAddAudience,              name='dbManagerAddAudience'),
    path('dbManagerHome/addDirector/',                  dbmViews.dbManagerAddDirector,              name='dbManagerAddDirector'),
    path('dbManagerHome/deleteAudience/',               dbmViews.dbManagerDeleteAudience,           name='dbManagerDeleteAudience'),
    path('dbManagerHome/addPlatform',                   dbmViews.dbManagerAddPlatform,              name='dbManagerAddPlatform'),
    path('dbManagerHome/updateDirectorPlatform',        dbmViews.dbManagerUpdateDirectorPlatform,   name='dbManagerUpdateDirectorPlatform'),
    path('dbManagerHome/list/<str:operation>',          dbmViews.dbManagerList,                     name='dbManagerList'),

    path('directorHome/',                               drtViews.directorHome,                      name='drtHome'),
    path('directorHome/addPredecessor/',                drtViews.drtAddPredecessor,                 name='drtAddPredecessor'),
    path('directorHome/addMovie/',                      drtViews.drtAddMovie,                       name='drtAddMovie'),
    path('directorHome/addTheatre/',                    drtViews.drtAddTheatre,                     name='drtAddTheatre'),
    path('directorHome/addSession/',                    drtViews.drtAddSession,                     name='drtAddSession'),
    path('directorHome/updateMovieName/',               drtViews.drtUpdateMovieName,                name='drtUpdateMovieName'),
    path('directorHome/list/<str:listingOperation>/',   drtViews.directorList,                      name='drtList'),


    path('audienceHome/',                               audViews.audienceHome,                      name='audHome'),
    path('audienceHome/buyTicket/',                     audViews.audienceBuyTicket,                 name='audBuyTicket'),
    path('audienceHome/rate/',                          audViews.audienceRate,                      name='audRate'),
    path('audienceHome/list/<str:listingOperation>/',   audViews.audienceList,                      name='audList'),
    
]


