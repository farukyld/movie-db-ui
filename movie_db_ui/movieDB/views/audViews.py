from ..constants import(
    AudListingOperations as __AudListingOperations,
    AUD_LISTING_OPERATIONS as __LISTING_OPERATIONS,
    UserTypes as __UserTypes,
)
from ..forms.audForms import(
    BuyTicketForm as __BuyTicketForm,
    RateMovieForm as __RateMovieForm,
)
from ..databaseManagement.serverInteractors.audienceInteractions import (
    buyTicket as __buyTicket,
    listBoughtTickets as __listBoughtTickets,
    listSessions as __listSessions,
    rate as __rate,
    previewTicket as __previewTicket,
)
from django.shortcuts import render as __render
from ..sessionTracking import sessionCheck as __sessionCheck
from django.http import HttpResponseNotFound as __HttpResponseNotFound



__wantedUserType=__UserTypes.AUDIENCE

def audienceHome(request):
    sessionCorrect,resp=__sessionCheck(request,__wantedUserType)
    if not sessionCorrect:
        return resp
    context = {'listingOperations':__LISTING_OPERATIONS}
    return __render(request,'movieDB/audience/audienceHomepage.html',context)


def audienceBuyTicket(request):
    sessionCorrect, resp_sess = __sessionCheck(request, __wantedUserType)
    if not sessionCorrect:
        return resp_sess
    session = resp_sess

    context = {'form':__BuyTicketForm(),'formHeader':'Buy Ticket', 'includePreviewButton':True}
    
    form = __BuyTicketForm(request.POST or None)
    if form.is_valid():
        if request.POST and 'preview' in request.POST:
            success,headers,data=__previewTicket(form.cleaned_data['sessionId'])
            context['headers']=headers
            context['data']=data
        elif request.POST and 'submit' in request.POST:
            success,message=__buyTicket(
                session['username'],
                form.cleaned_data['sessionId'])
            context['message']=message
    elif request.method =='POST':
        context['message']='invalid input'
    return __render(request, 'movieDB/audience/addOperations.html',context)



def audienceRate(request):
    sessionCorrect, resp_sess = __sessionCheck(request, __wantedUserType)
    if not sessionCorrect:
        return resp_sess
    session = resp_sess

    context = {'form':__RateMovieForm(),'formHeader':'Rate Movie'}

    form = __RateMovieForm(request.POST or None)
    if form.is_valid():
        success, message = __rate(
            session['username'],
            form.cleaned_data['movieId'],
            form.cleaned_data['points'])
        context['message'] = message
    elif request.method == 'POST':
        context['message'] = 'Invalid input'
    return __render(request, 'movieDB/audience/addOperations.html', context)


def audienceList(request, listingOperation):
    sessionCorrect, resp_sess = __sessionCheck(request, __wantedUserType)
    if not sessionCorrect:
        return resp_sess
    session = resp_sess

    if listingOperation == __AudListingOperations.SESSIONS.value:
        success, headers, data = __listSessions()
        tableName = "Movie Sessions"
        context = {'headers': headers, 'data': data, 'tableName': tableName}

    elif listingOperation == __AudListingOperations.BOUGHT_TICKETS.value:
        success, headers, data = __listBoughtTickets(session['username'])
        tableName = "Tickets You Bought"
        context = {'headers': headers, 'data': data, 'tableName': tableName}
    else:
        return __HttpResponseNotFound('<h1>Page not found</h1>')
    return __render(request, 'movieDB/audience/audienceList.html', context)
