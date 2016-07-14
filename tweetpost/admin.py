from django.contrib import admin

# Register your models here.

from .models import Tweet, HashTag, Comment, Like

admin.site.register(Tweet)
admin.site.register(HashTag)
admin.site.register(Comment)
admin.site.register(Like)
