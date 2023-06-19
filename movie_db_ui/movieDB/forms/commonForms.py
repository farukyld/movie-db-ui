from django import forms
from ..constants import USER_TYPES as _USER_TYPES

# I had to use _USER_TYPES with single _ because of name mangling
# IN python if there is a name exists with double _
# it counts this name as a class field, ignoring module namespace.

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    userType = forms.ChoiceField(choices=_USER_TYPES)
