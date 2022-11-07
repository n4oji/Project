from django import forms 
from django.forms import ModelForm
from .models import Venue,Event

class VenueForm(ModelForm):
	class Meta:
		model = Venue
		# fields = "__all__"
		fields = ('name', 'address', 'zip_code', 'phone', 'website', 'email_address')
		labels = {
			'name': '',
			'address': '',
			'zip_code': '',
			'phone': '',
			'website': '',
			'email_address': '',
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue Name'}),
			'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
			'zip_code': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip-Code'}),
			'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),
			'website': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Website'}),
			'email_address': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}),
		}

class EventForm(ModelForm):
	class Meta:
		model = Event
		# fields = "__all__"
		fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description')
		labels = {
			'name': '',
			'event_date': 'YYYY-MM-DD HH:MM:SS',
			'venue': 'Venue',
			'manager': 'Manager',
			'attendees': 'Attendees',
			'description': '',
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
			'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Date'}),
			'venue': forms.Select(attrs={'class':'form-select','placeholder':'Venue'}),
			'manager': forms.Select(attrs={'class':'form-select', 'placeholder':'Manager'}),
			'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Attendees'}),
			'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
		}