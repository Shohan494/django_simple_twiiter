from __future__ import unicode_literals

from django.db import models

# Create your models here.

from tweet.models import UserProfile

# the tweet model defines users post, posted time, likes on post
class Tweet(models.Model):
    # when the tweet post is added, that time
    added = models.DateTimeField(auto_now_add=True)
    # who tweeted, relation goes ForeignKey with the "UserProfile" model of "tweet" app
    tweeter = models.ForeignKey(UserProfile, related_name='user_tweets')
    # the weet post content
    content = models.TextField(max_length=140)
    # like on the 'specific each post'
    # this is not used yet
    likes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.content

# for hash_# tagged post
class HashTag(models.Model):
    # tha hash (#) tag
    tag = models.CharField(max_length=140)
    # when added
    added = models.DateTimeField(auto_now_add=True)
    # number of this 'specific each hashtag'
    # this is from "convert_hashtag_to_link"
    number = models.IntegerField(default=0)

    # the hashtag __unicode__, it will be used when needed(etc: in admin)
    def __unicode__(self):
        return u'%s tagged %d times' % (self.tag, self.number)

    class Meta:
        # tag must be unique "???"
        unique_together = ('tag',)

class Comment(models.Model):
    # each comment will belong to some specific tweet post
    # so the relation will be ForeignKey to the "Tweet" model
    # related name is set "comments"
    # The related_name option in models.ForeignKey allows us to have access to comments from within the Post model.
    tweet = models.ForeignKey('Tweet', related_name='comments')
    # author means who commented, there will be a field to fill it
    # REMINDER: IT WILL BE BETTER IF THE AUTHOR IS A REGISTERD USER
    # but in this case, there is a option called approving comments
    author = models.CharField(max_length=200)
    # comment field
    text = models.TextField()
    # comment created date
    created_date = models.DateTimeField(auto_now_add=True)
    # comment mustr be approved by the ADMIN or optional(registed users)
    approved_comment = models.BooleanField(default=False)

    # the comment approving method
    def approve(self):
        self.approved_comment = True
        self.save()

    # string reperesntation of the comment, it will be used when needed
    def __str__(self):
        return self.text
