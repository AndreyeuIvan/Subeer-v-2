from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.generic.base import View
from django.db.models import Q
import requests
from .models import Serial, Episode, Category, UserProfile
from .form import NameForm, CategoryForm, SerialForm, UserForm, UserProfileForm
from django.utils import timezone
from registration.backends.simple.views import RegistrationView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def rating(request):

	rates = Serial.objects.order_by('rate')
	paginator = Paginator(rates, 3)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'rating.html', {'page_obj': page_obj})


def new_episodes(request):

	new_episode = Episode.objects.order_by('date_of_adding')
	paginator = Paginator(new_episode, 1)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'new_episodes.html', {'page_obj': page_obj})


def new_serials(request):

	new_serials = Serial.objects.order_by('date_of_release')
	paginator = Paginator(new_serials, 3)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'new_serials.html', {'page_obj': page_obj})


def get_serial(request, slug):
	serial = Serial.objects.get(url=slug)
	episodes = Episode.objects.filter(serial_id=serial.id)
	return render(request, 'serial_details.html', {'serial':serial, 'episodes':episodes})


class EpisodeDetailView(View):
	pass


def serial_new(request):
    if request.method == "POST":
        form = SerialForm(request.POST)
        if form.is_valid():
            serial = form.save(commit=False)
            serial.save()
            return redirect('serial_details', pk=serial.pk)
    else:
        form = SerialForm()
    return render(request, 'serial_edit.html', {'form': form})


'''def serial_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = SerialForm(request.POST, instance=serial)
        if form.is_valid():
            serial = form.save(commit=False)
            serial.save()
            return redirect('serial_details', pk=serial.pk)
    else:
        form = SerialForm(instance=serial)
    return render(request, 'serial_edit.html', {'form': form})'''


class AddReview(View):
	pass
"""Отзывы

	def post(self, request, pk):
		form = ReviewForm(request.POST)
		movie = Serial.objects.get(id= pk)
		if form.is_valid():
			form = form.save(commit=False)
			if request.POST.get("parent", None):
				form.parent_id = int(request.POST.get("parent"))
			form.movie = movie
			form.save()
		return redirect(movie.get_absolute_url())"""


'''Here I want to practice rest api'''
def rest(request):
	user = {}
	if 'username' in request.GET:
		username = request.GET['username']
		url = 'https://api.github.com/users/%s' % username
		r = requests.get(url)
		search_was_succesful = (r.status_code == 200)
		search_result = r.json()
		search_result['success'] = search_was_succesful
		search_result['rate'] = {
			'limit': r.headers['X-Ratelimit-Limit'],
			'remaining': r.headers['X-Ratelimit-Remaining']
		}
	return render(request, 'rest.html', {'search_result': search_result})


def get_name(request):
	if request.method == 'GET':
		form = NameForm()
		return render(request, 'form.html', {'form': form})
	elif request.method == 'POST':
		form = NameForm(request.POST)
		feedback = form.save()
		feedback.save()
		return render(request, 'form.html', {'form': NameForm()} )
	else:
		return HttpResponseNotAllowed()


#Creating form in order to change or add Category 
def category_show(request, pk):
	categories = get_object_or_404(Category,pk=pk)
	return render(request, 'category_details.html', {'categories': categories})


def category_new(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			category = form.save(commit=False)
			category.save()
			return category_show(request, pk=category.pk)
	else:
		form = CategoryForm()
	return render(request, 'form.html', {'form':form})


def category_edit(request, pk):
	category = get_object_or_404(Category, pk=pk)
	if request.method == 'POST':
		form = CategoryForm(request.POST, instance=category)
		if form.is_valid():
			category = form.save(commit=False)
			category.save()
			return category_show(request, pk=category.pk)
	else:
		form = CategoryForm(instance=category)
	return render(request, 'category_edit.html', {'form': form})


#Creating Serial form in order to chage and add category
def search_serial(request):
	
	query = request.GET.get('q')
	if query:
		serials = Serial.objects.filter(
			Q(title__icontains=query))
		return serial_show(request, pk=serials.values()[0]['id'])
	else:
		return serial_all(request)


def serial_list(request):
	serials = Serial.objects.all()
	paginator = Paginator(serials, 3)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'serial_all.html', {'page_obj': page_obj})


def serial_show(request, pk):
	'''Here I want to show list of Serials'''
	serials = get_object_or_404(Serial, pk=pk)
	return render(request, 'serial_show.html', {'serials': serials})


def serial_new(request):
	if request.method == 'POST':
		form = SerialForm(request.POST)
		if form.is_valid():
			serial = form.save(commit=False)
			serial.date_of_release = timezone.now()
			serial.save()
			return serial_list(request)
	else:
		form = SerialForm()
	return render(request, 'form.html', {'form':form})


def serial_edit(request,pk):
	serial = get_object_or_404(Serial, pk=pk)
	if request.method == 'POST':
		form = CategoryForm(request.POST, instance=serial)
		if form.is_valid():
			serial = form.save(commit=False)
			serial.save()
			return serial_list(request, pk=serial.pk)
	else:
		form = CategoryForm(instance=serial)
	return render(request, 'serial_edit.html', {'form':form})

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
		return render(request, 'registration/login.html')


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
	return HttpResponseRedirect(reverse('index'))

# Create a new class that redirects the user to the index page,
#if successful at logging
class My(RegistrationView):
	def get_success_url(self, user):
		return ''