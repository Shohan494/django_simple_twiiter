from django.contrib import admin

# Register your models here.

from .models import UserProfile, Relation

admin.site.register(UserProfile)
admin.site.register(Relation)
