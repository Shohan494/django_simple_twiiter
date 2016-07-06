from django.contrib import admin

# Register your models here.

from .models import Tweet, HashTag

admin.site.register(Tweet)
admin.site.register(HashTag)
