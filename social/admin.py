from django.contrib import admin

from social.models import Person, Post, Profile

# Register your models here.
admin.site.register(Person)
admin.site.register(Post)
admin.site.register(Profile)
