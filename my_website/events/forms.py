from django import forms 
from django.forms import ModelForm
from .models import Venue 

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
