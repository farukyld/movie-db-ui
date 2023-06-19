from ..forms.dbmForms import ( 
    AddAudienceForm as __AddAudienceForm,
    AddDirectorForm as __AddDirectorForm,
    DeleteAudienceForm as __DeleteAudienceForm,
    AddPlatformForm as __AddPlatformForm,
    UpdateDirectorPlatformForm as __UpdateDirectorPlatformForm,
    AudienceRatingsForm as __AudienceRatingsForm,
    DirectorSessionsForm as __DirectorSessionsForm,
    MovieOverallRatingForm as __MovieOverallRatingForm)
from ..databaseManagement.serverInteractors.dbManagerInteractions import (
    addAudience as __addAudience,
    addDirector as __addDirector,
    deleteAudience as __deleteAudience,
    addPlatform as __addPlatform,
    updateDirectorPlatform as __updateDirectorPlatform,
    listAudience as __listAudience,
    listDirectors as __listDirectors,
    listPlatforms as __listPlatforms,
    listRatings_ofAudience as __listRatings_ofAudience,
    listSessions_ofDirector as __listSessions_ofDirector,
    viewOverallRating as __viewOverallRating,
    )
from ..constants import (
    UserTypes as __UserTypes,
    DBM_ListingOperation as __ListingOperation,
    DBM_LISTING_OPERATIONS as __LISTING_OPERATIONS)
from django.shortcuts import render as __render
from ..sessionTracking import sessionCheck as __sessionCheck


__wantedUserType=__UserTypes.DB_MANAGER

def dbManagerHome(request):
    sessionCorrect,resp=__sessionCheck(request,__wantedUserType)
    if not sessionCorrect:
        return resp
    context = {'listingOperations':__LISTING_OPERATIONS}
    return __render(request,'movieDB/dbManager/dbManagerHome.html',context)

def dbManagerAddAudience(request):
    sessionCorrect,resp_session=__sessionCheck(request,__wantedUserType)
    if not sessionCorrect:
        return resp_session
    form = __AddAudienceForm(request.POST or None)
    if form.is_valid():
        success, message = __addAudience(form.cleaned_data['name'],
                                        form.cleaned_data['surname'],
                                        form.cleaned_data['userName'],
                                        form.cleaned_data['userPassword'])
        context = {'form':__AddAudienceForm(),'message':message} 
        return __render(request, 'movieDB/dbManager/addAudience.html',context )
    context = {'form':__AddAudienceForm()} 
    if request.method=='POST': 
        context['message']='invalid input' # this part will execute if request method is post and form is invalid.
    return __render(request, 'movieDB/dbManager/addAudience.html', context)



def dbManagerAddDirector(request):
    sessionCorrect,resp_session=__sessionCheck(request,__wantedUserType)
    if not sessionCorrect:
        return resp_session
    form = __AddDirectorForm(request.POST or None)
    if form.is_valid():
        success, message =__addDirector(form.cleaned_data['username'], 
                        form.cleaned_data['userPassword'], 
                    form.cleaned_data['firstName'], 
                    form.cleaned_data['surname'], 
                    form.cleaned_data['nation'], 
                    form.cleaned_data['ratingPlatformId'])
        context = {'form':__AddDirectorForm(),'message':message} 

        return __render(request, 'movieDB/dbManager/addDirector.html', context)
    context = {'form':__AddDirectorForm()} 
    if request.method=='POST': 
        context['message']='invalid input' # this part will execute if request method is post and form is invalid.
    return __render(request, 'movieDB/dbManager/addDirector.html',context)



def dbManagerDeleteAudience(request):
    sessionCorrect, resp_session = __sessionCheck(request,__wantedUserType)
    if not sessionCorrect:
        return resp_session
    form = __DeleteAudienceForm(request.POST or None)
    if form.is_valid():
        success, message = __deleteAudience(form.cleaned_data['username'])
        context = {'form':__DeleteAudienceForm(),'message':message} 
        return __render(request, 'movieDB/dbManager/deleteAudience.html', context)
    context = {'form':__DeleteAudienceForm()} 
    if request.method=='POST': 
        context['message']='invalid input' # this part will execute if request method is post and form is invalid.
    return __render(request, 'movieDB/dbManager/deleteAudience.html', context)


def dbManagerAddPlatform(request):
    sessionCorrect, resp_session = __sessionCheck(request,__wantedUserType)
    if not sessionCorrect:
        return resp_session
    form = __AddPlatformForm(request.POST or None)
    if form.is_valid():
        success, message = __addPlatform( form.cleaned_data['platformName'])
        context = {'message':message,'form':__AddPlatformForm()}
        return __render(request, 'movieDB/dbManager/addPlatform.html',context)
    context = {'form':__AddPlatformForm()} 
    if request.method=='POST': 
        context['message']='invalid input' # this part will execute if request method is post and form is invalid.
    return __render(request, 'movieDB/dbManager/addPlatform.html', context)


def dbManagerUpdateDirectorPlatform(request):
    sessionCorrect, resp_session = __sessionCheck(request,__wantedUserType)
    if not sessionCorrect:
        return resp_session
    form = __UpdateDirectorPlatformForm(request.POST or None)
    if form.is_valid():
        success, message = __updateDirectorPlatform(
            form.cleaned_data['username'], 
            form.cleaned_data['platform_id'])
        context = {'message':message,'form':__UpdateDirectorPlatformForm()}
        return __render(request, 'movieDB/dbManager/updateDirectorPlatform.html', context)
    context = {'form':__UpdateDirectorPlatformForm()} 
    if request.method=='POST': 
        context['message']='invalid input' # this part will execute if request method is post and form is invalid.
    return __render(request, 'movieDB/dbManager/updateDirectorPlatform.html', context)


def dbManagerList(request, operation):
    sessionCorrect, resp_session = __sessionCheck(request,__wantedUserType)
    if not sessionCorrect:
        return resp_session

    if operation == __ListingOperation.DIRECTORS.value:
        success, headers, data = __listDirectors()
        return __render(request, 'movieDB/dbManager/listDirectors.html', {'data': data, 'headers': headers})

    elif operation == __ListingOperation.PLATFORMS.value:
        success, headers, data = __listPlatforms()
        return __render(request, 'movieDB/dbManager/listPlatforms.html', {'data': data, 'headers': headers})

    elif operation == __ListingOperation.AUDIENCE.value:
        success, headers, data = __listAudience()
        return __render(request, 'movieDB/dbManager/listAudience.html', {'data': data, 'headers': headers})

    elif operation == __ListingOperation.AUDIENCE_RATINGS.value:
        form = __AudienceRatingsForm(request.POST or None) 
        if form.is_valid():
            audienceUsername=form.cleaned_data['username']
            success, headers, data = __listRatings_ofAudience(audienceUsername)
            context={'data': data,'username':audienceUsername, 'headers': headers}
            return __render(request, 'movieDB/dbManager/listAudienceRatings.html',context )
        context = {'form':__AudienceRatingsForm()} 
        if request.method=='POST':
            context['message']='invalid input' # this part will execute if request method is post and form is invalid.
        return __render(request, 'movieDB/dbManager/listAudienceRatings.html',context)

    elif operation == __ListingOperation.DIRECTOR_SESSIONS.value:
        form = __DirectorSessionsForm(request.POST or None)
        if form.is_valid():
            directorUsername=form.cleaned_data['username']
            success, headers, data = __listSessions_ofDirector(directorUsername)
            context={'directorUsername':directorUsername,'data': data, 'headers': headers}
            return __render(request, 'movieDB/dbManager/listDirectorSessions.html', context)
        context = {'form':__DirectorSessionsForm()} 
        if request.method=='POST': 
            context['message']='invalid input' # this part will execute if request method is post and form is invalid.
        return __render(request, 'movieDB/dbManager/listDirectorSessions.html',context)

    elif operation == __ListingOperation.MOVIE_OVERALL_RATING.value:
        form = __MovieOverallRatingForm(request.POST or None)
        if form.is_valid():
            movieId = form.cleaned_data['movieId']
            success, headers, data = __viewOverallRating(movieId)
            context={'movieId':movieId, 'data': data, 'headers': headers}
            return __render(request, 'movieDB/dbManager/viewMovieOverallRating.html',context )
        context = {'form':__MovieOverallRatingForm()} 
        if request.method=='POST': 
            context['message']='invalid input' # this part will execute if request method is post and form is invalid.
        return __render(request, 'movieDB/dbManager/viewMovieOverallRating.html', context)
    