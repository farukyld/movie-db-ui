from typing import Dict as __Dict, Any as __Any
from secrets import token_hex as __token_hex
from django.urls import reverse as __reverse
from django.shortcuts import redirect as __redirect
from ..constants import UserTypes as __UserTypes


__sessions:__Dict[str,__Dict[str, __Any]]={}



def __generateSessionId():
    return str(__token_hex(16))


def createSession(username:str, userType:str):
    session = {'username':username, 'userType': userType}
    sessionID=__generateSessionId()
    __sessions[sessionID]=session
    return sessionID



def sessionCheck(request,wantedUserType:__UserTypes):
    sessionID = request.COOKIES.get('sessionID', None)
    if sessionID is None or __sessions.get(sessionID, {}).get('userType', None) != wantedUserType:
        url = __reverse('loginIndex_',kwargs={'message':'you should have logged in as '+ wantedUserType.displayName})
        response = __redirect(url)
        return False,response
    return True, __sessions[sessionID]