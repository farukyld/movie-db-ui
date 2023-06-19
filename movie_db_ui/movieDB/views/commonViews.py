from django.shortcuts import render as __render, redirect as __redirect 
from ..databaseManagement.serverInteractors.startUp import createTables as __createTables, insertInitialRecords as __insertInitialRecords
from ..databaseManagement.serverInteractors.checkCred import checkCredAudience as __checkCredAudience, checkCredDB_manager as __checkCredDB_manager, checkCredDirector as __checkCredDirector
from django.http import HttpResponse
from ..sessionTracking import createSession as __createSession
from ..forms.commonForms import LoginForm as __LoginForm
from django.urls import reverse as __reverse
from ..constants import UserTypes as __UserTypes, USER_TYPES as __USER_TYPES 


def index(request):
    return __render(request,'movieDB/index.html')


def createTables(request):
    success,content = __createTables()
    if success:
        return HttpResponse("tables created by reading "+str(content))
    else:
        return HttpResponse("tables already created ")
    

def insertInitialRecords(request):
    success, content = __insertInitialRecords()
    if success:
        return HttpResponse("values inserted by reading "+str(content))
    else:
        return HttpResponse("error at movieDB.insertInitialRecords: " + str(content))


def loginIndex(request,message=None):
    return __render(request,'movieDB/login.html',{'form':__LoginForm(),'message':message,'userTypes':__USER_TYPES})


def login(request):
    if request.method == "POST":
        form = __LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            userType = form.cleaned_data["userType"]
            if userType == "DB_Manager" and __checkCredDB_manager(username, password):
                sessionID = __createSession(username,__UserTypes.DB_MANAGER)
                response = __redirect('../dbManagerHome/')
                response.set_cookie('sessionID',sessionID)
                return response
            elif userType == "Audience" and __checkCredAudience(username, password):
                sessionID = __createSession(username,__UserTypes.AUDIENCE)
                response = __redirect('../audienceHome/')
                response.set_cookie('sessionID',sessionID)
                return response
            elif userType == "Director" and __checkCredDirector(username, password):
                sessionID = __createSession(username,__UserTypes.DIRECTOR)
                response = __redirect('../directorHome/')
                response.set_cookie('sessionID',sessionID)
                return response
            else:
                url=__reverse('loginIndex_',kwargs={'message':'invalid credentials for '+userType})
                return __redirect(url)
        url=__reverse('loginIndex_',kwargs={'message':'invalid form '})
        return __redirect(url)
    return __redirect('loginIndex')