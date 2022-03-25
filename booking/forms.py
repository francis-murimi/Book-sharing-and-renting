from django import forms
from django.forms.widgets import DateInput
from .models import Booking

class BookingProcessForm(forms.ModelForm):
    class Meta:
        model = Booking
        #fields = ['booking_type','delivery_date','duration','payed']
        exclude = ['user','book','kitabu']


class DateForm(forms.Form):
    delivery_date = forms.DateField(widget=DateInput())
