from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Category(models.Model):
	'Category'
	name = models.CharField("Категория", max_length=150)
	description = models.TextField("Описание")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Категория"
		verbose_name_plural = "Категории"


class Serial(models.Model):
	"""Serials"""
	title = models.CharField("Название", max_length=100)
	description = models.TextField("Описание")
	#poster = models.ImageField("Постер", upload_to="static/img/")
	category = models.ForeignKey(
		Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
	)
	date_of_release = models.DateField("Date of premiere", default=date.today)
	rate = models.SmallIntegerField("Значение", default=0)
	url = models.SlugField(max_length=130)

	def __str__(self):
		return self.title

	#def get_absolute_url(self):
	#	return reverse("serial_detail", kwargs={"slug": self.url})

	#def get_review(self):
	#	return self.reviews_set.filter(parent__isnull=True)

	class Meta:
		verbose_name = "Serial"

class Episode(models.Model):
	'Episode'
	title = models.CharField("Название", max_length=100)
	serial_id = models.ForeignKey(
		Serial, verbose_name="Serial_id", on_delete=models.SET_NULL, null=True
	)
	season = models.BigIntegerField(default=1)
	date_of_adding = models.DateField("Date of adding episode", default=date.today)
	url = models.TextField(unique=True)
	
	def __str__(self):
		return self.title

class Opinion(models.Model):
	BIO = models.CharField(max_length=100)
	Issue = models.CharField(max_length=100)
	Description = models.TextField()
	date_issue = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
	'''Creating user model in order to have data stored into db'''
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to = 'profile_images', blank=True)


	def __str__(self):
		return self.user.username