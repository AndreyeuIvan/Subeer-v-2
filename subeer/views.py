from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Serial, Episode, Category
from django.views.generic.base import View
from django.db.models import Q
import requests
from .form import NameForm, CategoryForm


def serial_list(request):
	
	serials = Serial.objects.all()
	paginator = Paginator(serials, 2)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'serial_all.html', {'page_obj': page_obj})


def rating(request):

	rates = Serial.objects.order_by('rate')
	paginator = Paginator(rates, 3)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'rating.html', {'page_obj': page_obj})


def new_episodes(request):

	new_episode = Episode.objects.order_by('date_of_adding')
	paginator = Paginator(new_episode, 3)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'new_episodes.html', {'page_obj': page_obj})


def new_serials(request):

	new_serials = Serial.objects.order_by('date_of_release')
	paginator = Paginator(new_serials, 3)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'new_serials.html', {'page_obj': page_obj})


class SerialDetailView(View):
	
	def get_serial(self, request, slug):
		serial = Serial.objects.get(url=slug)
		episodes = Episode.objects.filter(serial_id=serial.id)
		return render(request, 'serial_details.html', {'serial':serial, 'episodes':episodes})


class EpisodeDetailView(View):
	pass


def search_serial(request):

	query = request.GET.get('q')

	if query:
		serials = Serial.objects.filter(
			Q(title__icontains=query))
	else:
		serials = Serial.objects.all()
	return render(request , 'search_serial.html', {'serials':serials})


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