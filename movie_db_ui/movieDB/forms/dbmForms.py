from django import forms as _forms

class AddAudienceForm(_forms.Form):
    name = _forms.CharField(label='Name', max_length=100)
    surname = _forms.CharField(label='Surname', max_length=100)
    userName = _forms.CharField(label='Username', max_length=100)
    userPassword = _forms.CharField(label='Password', max_length=100, widget=_forms.PasswordInput)



class AddDirectorForm(_forms.Form):
    username = _forms.CharField(label='User Name', max_length=100)
    userPassword = _forms.CharField(label='User Password', widget=_forms.PasswordInput())
    firstName = _forms.CharField(label='First Name', max_length=100)
    surname = _forms.CharField(label='Surname', max_length=100)
    nation = _forms.CharField(label='Nation', max_length=50)
    ratingPlatformId = _forms.IntegerField(label='Rating Platform ID', required=False,min_value=0)


class DeleteAudienceForm(_forms.Form):
    username = _forms.CharField(label='User Name', max_length=100)


class AddPlatformForm(_forms.Form):
    platformName = _forms.CharField(max_length=255, label='Platform Name')


class UpdateDirectorPlatformForm(_forms.Form):
    username = _forms.CharField(label='Director Username', max_length=100)
    platform_id = _forms.IntegerField(label='New Platform ID',required=False)


class AudienceRatingsForm(_forms.Form):
    username = _forms.CharField(label='Audience Username', max_length=50)


class DirectorSessionsForm(_forms.Form):
    username = _forms.CharField(label='Director Username', max_length=50)


class MovieOverallRatingForm(_forms.Form):
    movieId = _forms.IntegerField(label='Movie ID')
