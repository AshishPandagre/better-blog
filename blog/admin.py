from django.contrib import admin
from .models import *

class BlogAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ['title',]}

admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag)
admin.site.register(Comment)