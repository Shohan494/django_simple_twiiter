from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User

# application users profile class
class UserProfile(models.Model):
    # user will be unique, so one2one relation
    user = models.OneToOneField(User, related_name='profile')
    # users relation will be many2many, so m2m relation

    relation = models.ManyToManyField(
        'self', # referencing to the UserProfile class(basically 'user')
        through='Relation',
        symmetrical=False,
        related_name='related_to',
        default=None
    )

    def __unicode__(self):
        return self.user.get_full_name()

    # To make sure that every new user gets his user profile instance created
    def create_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=user)
        post_save.connect(create_profile, sender=User)

class Relation(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='follows')
    is_followed = models.ForeignKey(UserProfile, related_name='followers')
    follow_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s follows %s' % (self.follower.user.username, self.is_followed.user.username)

    class Meta:
        unique_together = ('follower', 'is_followed')
