from django import forms as _forms



class PredecessorForm(_forms.Form):
    predecessor_id = _forms.IntegerField(label="Predecessor Movie ID")
    successor_id = _forms.IntegerField(label="Successor Movie ID")


class AddMovieForm(_forms.Form):
    movie_name = _forms.CharField(max_length=255, label='Movie Name')
    duration = _forms.IntegerField(label='Duration', min_value=1)
    genres = _forms.CharField(
        max_length=255, 
        label='Genre(s)', 
        help_text='Enter genres separated by comma (e.g. "Action, Adventure")'
    )
    
    def clean_genre(self):
        genre_string = self.cleaned_data['genres']
        genres = [genre.strip() for genre in genre_string.split(",")]
        return genres


class AddTheatreForm(_forms.Form):
    theatreName = _forms.CharField(label='Theatre Name', max_length=100)
    theatreDistrict = _forms.CharField(label='Theatre District', max_length=100)
    theatreCapacity = _forms.IntegerField(label='Theatre Capacity', min_value=1)


class AddSessionForm(_forms.Form):
    movieId = _forms.IntegerField(label='Movie ID')
    theatreId = _forms.IntegerField(label='Theatre ID')
    timeslot = _forms.IntegerField(label='Timeslot (0-4)', min_value=0, max_value=4)
    date = _forms.DateField(label='Date (MM/DD/YY)', input_formats=['%m/%d/%y'])


class UpdateMovieNameForm(_forms.Form):
    movieId = _forms.IntegerField(label='Movie ID')
    movieName = _forms.CharField(max_length=50, label='New Movie Name')


class AvailableTheatresForm(_forms.Form):
    date = _forms.DateField(label='Date (MM/DD/YY)', input_formats=['%m/%d/%y'])
    slot = _forms.IntegerField(label='Slot', min_value=0, max_value=4)
    duration = _forms.IntegerField(label='Duration', min_value=0, max_value=4)

class MovieAudienceForm(_forms.Form):
    movieId = _forms.IntegerField(label='Movie ID')
