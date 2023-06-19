from django import forms as _forms

class BuyTicketForm(_forms.Form):
    sessionId = _forms.IntegerField(
        min_value=1, 
        required=True,
        widget=_forms.NumberInput(attrs={'class': 'form-control'}), 
        label='Session ID'
    )

class RateMovieForm(_forms.Form):
    points = _forms.FloatField(
        min_value=0.0,
        max_value=5.0,
        required=True,
        widget=_forms.NumberInput(attrs={'class': 'form-control'}),
        label='Points'
    )
    movieId = _forms.IntegerField(
        min_value=1,
        required=True,
        widget=_forms.NumberInput(attrs={'class': 'form-control'}), 
        label='Movie ID'
    )
