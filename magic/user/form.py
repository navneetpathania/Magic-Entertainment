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
	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('This email address is already in use. Please use a different email address.')
		return email
class userUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username','email']

class profileUpdateForm(forms.ModelForm):
	class Meta:
		model = CreateProfile
		fields = ['image']