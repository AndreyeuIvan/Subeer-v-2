from django.forms import ModelForm
from django import forms
from .models import Category, Opinion, Serial, UserProfile 
from django.contrib.auth.models import User



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


class SerialForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text='Enter name of Serial.')
	description = forms.CharField(max_length=256, help_text='Enter description.')
	url = forms.SlugField(help_text='Please enter the URL of page.')
	

	class Meta:
		model = Serial
		fields = ['title', 'description', 'category', 'date_of_release']


class UserForm(forms.ModelForm):
    '''Creating an user form, for intering data'''
    password = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

