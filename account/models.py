from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	'''Creating user model in order to have data stored into db'''
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to = 'profile_images', blank=True)


	def __str__(self):
		return self.user.username