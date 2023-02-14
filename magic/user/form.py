from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CreateProfile



class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username','email','password1','password2']
		help_texts = {
            'username': None,
            'email': None,
            'password': None,
        	}
class userUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username','email']

class profileUpdateForm(forms.ModelForm):
	class Meta:
		model = CreateProfile
		fields = ['image']