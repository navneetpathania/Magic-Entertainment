from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .form import UserRegisterForm,userUpdateForm,profileUpdateForm
from django.contrib import messages
from .models import CreateProfile
from django.contrib.auth.decorators import login_required

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			messages.success(request,f'Account is crated for {username}')
			form.save()
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request,'user/register.html',{'form':form})

@login_required
def profile(request):
	if request.method == 'POST':
		u_form = userUpdateForm(request.POST,instance=request.user)
		i_form = profileUpdateForm(request.POST,request.FILES,instance=request.user.createprofile)
		if u_form.is_valid() and i_form.is_valid():
			u_form.save()
			i_form.save()
			messages.success(request,'Your account is updated successfully!')
			return redirect('profile')

	else:
		u_form = userUpdateForm(instance=request.user)
		i_form = profileUpdateForm(instance=request.user.createprofile)
		context = {
		'u_form':u_form,
		'i_form':i_form
		}
		return render(request,'user/profile.html',context)

