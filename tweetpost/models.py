from __future__ import unicode_literals

from django.db import models

# Create your models here.

from tweet.models import UserProfile

# the tweet model defines users post, posted time, likes on post
class Tweet(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    tweeter = models.ForeignKey(UserProfile, related_name='user_tweets')
    content = models.TextField(max_length=140)
    likes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.content
        
# for hash_# tagged post
class HashTag(models.Model):
    tag = models.CharField(max_length=140)
    added = models.DateTimeField(auto_now_add=True)
    number = models.IntegerField(default=0)

    class Meta:
        unique_together = ('tag',)

    def __unicode__(self):
        return u'%s tagged %d times' % (self.tag, self.number)
