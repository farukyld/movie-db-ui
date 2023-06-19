from ..databaseManagement.serverInteractors.directorInteractions import (
    addPredecessor as __addPredecessor,
    addMovie as __addMovie,
    addTheatre as __addTheatre,
    addSession as __addSession,
    updateMovieName as __updateMovieName,
    listAvailableTheatres as __getAvailableTheatres,
    getMovieAudience as __getMovieAudience,
    getSessionlessMovies as __getSessionlessMovies,
    getSessionsMovies as __getSessionsMovies,
)
from ..constants import (
    UserTypes as __UserTypes,
    DrtListingOperations as __DrtListingOperations,
    DRT_LISTING_OPERATIONS as __LISTING_OPERATIONS
)
from ..forms.drtForms import (
    PredecessorForm as __PredecessorForm,
    AddMovieForm as __AddMovieForm,
    AddTheatreForm as __AddTheatreForm,
    AddSessionForm as __AddSessionForm,
    UpdateMovieNameForm as __UpdateMovieNameForm,
    AvailableTheatresForm as __AvailableTheatresForm,
    MovieAudienceForm as __MovieAudienceForm,
)

from django.shortcuts import render as __render
from ..sessionTracking import sessionCheck as __sessionCheck
from django.http import HttpResponseNotFound as __HttpResponseNotFound


__wantedUserType = __UserTypes.DIRECTOR

def directorHome(request):
    sessionCorrect, resp = __sessionCheck(request, __wantedUserType)
    if not sessionCorrect:
        return resp
    context = {'listingOperations':__LISTING_OPERATIONS}
    return __render(request, 'movieDB/director/directorHomepage.html', context)



def drtAddPredecessor(request):
    sessionCorrect, resp_sess = __sessionCheck(request, __wantedUserType)
    if not sessionCorrect:
        return resp_sess
    session = resp_sess

    context = {'form':__PredecessorForm(),'formHeader':'Add Predecessor'}
    
    form = __PredecessorForm(request.POST or None)
    if form.is_valid():
        result, message = __addPredecessor(
            form.cleaned_data['predecessor_id'],
            form.cleaned_data['successor_id'])
        context['message'] = message
    elif  request.method=='POST':
        context['message']='invalid input' # this part will execute if request method is post and form is invalid.
    # in the case of request is get, the context won't contain a message. 
    return __render(request, 'movieDB/Director/addOperation.html', context)



def drtAddMovie(request):
    sessionCorrect, resp_sess = __sessionCheck(request, __wantedUserType)
    if not sessionCorrect:
        return resp_sess
    session = resp_sess

    context = {'form':__AddMovieForm(),'formHeader':'Add Movie'}

    form = __AddMovieForm(request.POST or None)
    if form.is_valid():
        success, message = __addMovie(
            session['username'],
            form.cleaned_data['movie_name'],
            form.cleaned_data['duration'],
            form.clean_genre())
        context['message'] = message
    elif request.method == 'POST':
        context['message'] = 'Invalid input' 
    return __render(request, 'movieDB/director/addOperation.html', context)


def drtAddTheatre(request):
    sessionCorrect, resp_sess = __sessionCheck(request, __wantedUserType)
    if not sessionCorrect:
        return resp_sess
    session = resp_sess

    context = {'form':__AddTheatreForm(),'formHeader':'Add Theatre'}

    form = __AddTheatreForm(request.POST or None)
    if form.is_valid():
        success, message = __addTheatre(
            session['username'],
            form.cleaned_data['theatreName'],
            form.cleaned_data['theatreDistrict'],
            form.cleaned_data['theatreCapacity'])
        context['message'] = message
    elif request.method == 'POST':
        context['message'] = 'Invalid input' 
    return __render(request, 'movieDB/director/addOperation.html', context)



def drtAddSession(request):
    sessionCorrect, resp_sess = __sessionCheck(request, __wantedUserType)
    if not sessionCorrect:
        return resp_sess
    session = resp_sess

    context = {'form':__AddSessionForm(),'formHeader':'Add Session'}

    form = __AddSessionForm(request.POST or None)
    if form.is_valid():
        success, message = __addSession(
            session['username'],
            form.cleaned_data['movieId'],
            form.cleaned_data['theatreId'],
            form.cleaned_data['timeslot'],
            form.cleaned_data['date'])
        context['message'] = message
    elif request.method == 'POST':
        context['message'] = 'Invalid input' 
    return __render(request, 'movieDB/director/addOperation.html', context)



def drtUpdateMovieName(request):
    sessionCorrect, resp_sess = __sessionCheck(request, __wantedUserType)
    if not sessionCorrect:
        return resp_sess
    session = resp_sess

    context = {'form':__UpdateMovieNameForm(),'formHeader':'Update Movie Name'}

    form = __UpdateMovieNameForm(request.POST or None)
    if form.is_valid():
        success, message = __updateMovieName(
            session['username'],
            form.cleaned_data['movieId'],
            form.cleaned_data['movieName'])
        context['message'] = message
    elif request.method == 'POST':
        context['message'] = 'Invalid input' 
    return __render(request, 'movieDB/director/addOperation.html', context)


def directorList(request, listingOperation):
    sessionCorrect, resp_sess = __sessionCheck(request, __wantedUserType)
    if not sessionCorrect:
        return resp_sess
    session = resp_sess

    if listingOperation == __DrtListingOperations.SLOT_AVAILABLE_THETRS.value:
        form = __AvailableTheatresForm(request.POST or None)

        context = {'form':__AvailableTheatresForm(),'formHeader': 'Available Theaters Form'}

        if form.is_valid():
            success, headers, data = __getAvailableTheatres(
                session['username'],
                form.cleaned_data['date'],
                form.cleaned_data['slot'],
                form.cleaned_data['duration'])
            tableName = "Available Theatres"
            context = {'headers': headers, 'data': data, 'tableName': tableName}
        elif request.method == 'POST':
            context['message'] = 'Invalid input'

    elif listingOperation == __DrtListingOperations.SESSIONS_MOVIES.value:
        success, headers, data = __getSessionsMovies(session['username'])
        tableName = "Sessions and Movies"
        context = {'headers': headers, 'data': data, 'tableName': tableName}

    elif listingOperation == __DrtListingOperations.MOVIE_AUDIENCE.value:
        form = __MovieAudienceForm(request.POST or None)
        context = {'form':__MovieAudienceForm(), 'formHeader':'Audience of a Movie Form'}

        if form.is_valid():
            success, headers, data = __getMovieAudience(
                session['username'],
                form.cleaned_data['movieId'])
            tableName = "Movie Audience"
            context = {'headers': headers, 'data': data, 'tableName': tableName}
        elif request.method == 'POST':
            context['message'] = 'Invalid input'

    elif listingOperation == __DrtListingOperations.SESSIONLESS_MOVIES.value:
        success, headers, data = __getSessionlessMovies(session['username'])
        tableName = "Movies without Session"
        context = {'headers': headers, 'data': data, 'tableName': tableName}

    else:
        return __HttpResponseNotFound('<h1>Page not found</h1>')
    return __render(request, 'movieDB/director/directorList.html', context)
