from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from subeer.views import serial_list
from .models import UserProfile
from .forms import UserForm, UserProfileForm

from registration.backends.simple.views import RegistrationView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# registration

def register(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()
			registered = True
		else:
			print(user_form.errors, profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	return render(request,
				 'registration/register.html',
				 {'user_form': user_form,
				 'profile_form':profile_form,
				 'registered':registered} )

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return serial_list(request)
			else:
				return HttpResponse('not allowed')
		else:
			print(f'Invalid login details: {username}, {password}')
	else:
		return render(request, 'registration/login_old.html')


def some_view(request):
	if not request.user.is_authenticated():
		return HttpResponse("You are logged in.")
	else:
		return HttpResponse("You are not logged in.")


@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)
	# Take the user back to the homepage.
	return serial_list(request)
