from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    def my_followers(self):
        return Relation.objects.filter(is_followed=self)

    def people_i_follow(self):
        return Relation.objects.filter(follower=self)

    def follow(self, person_to_follow):
        relation, created = Relation.objects.get_or_create(
            follower=self,
            is_followed=person_to_follow
        )
        return relation

    def unfollow(self, person_to_unfollow):
        try:
            Relation.objects.get(
                follower=self, is_followed=person_to_unfollow
            ).delete()
        except Relation.DoesNotExist:
            pass
        return

# To make sure that every new user gets his user profile instance created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class Relation(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='follows')
    is_followed = models.ForeignKey(UserProfile, related_name='followers')
    follow_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s follows %s' % (self.follower.user.username, self.is_followed.user.username)

    class Meta:
        unique_together = ('follower', 'is_followed')
