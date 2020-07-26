from django.contrib import admin
from .models import Category, Serial, Episode, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
	list_display_links = ('name',)


@admin.register(Serial)
class SerialAdmin(admin.ModelAdmin):
	list_display = ('title','category', 'date_of_release', 'rate')


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
	list_display = ('title', 'season', 'date_of_adding')
	list_filter = ('season', )
	search_fields = ('title', 'date_of_adding')


admin.site.register(UserProfile)
#admin.site.register(Category, CategoryAdmin)
#admin.site.register(Serial)
#admin.site.register(Episode)