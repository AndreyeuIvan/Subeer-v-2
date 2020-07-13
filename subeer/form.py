from django.forms import ModelForm
from django import forms
from .models import Category, Opinion



class NameForm(forms.ModelForm):
	
	class Meta:
		model = Opinion
		fields = ['BIO', 'Issue', 'Description']


class CategoryForm(forms.ModelForm):

	name = forms.CharField(max_length=128, help_text='Please enter the category name.')
	description = forms.CharField(max_length=500, help_text='Please, provide description.')


	class Meta:
		model = Category
		fields = ('name', 'description')
#class SerialForm(forms.ModelForm):

	#class Meta:
		#model = models.Serial
		#fields = ['title', 'description']


