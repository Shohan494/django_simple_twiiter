from django import template

from tweet.models import UserProfile
from tweetpost.models import Like, Tweet
import datetime

register = template.Library()

@register.simple_tag
def people_you_may_know(user_id):
    return UserProfile.objects.exclude(
        followers__follower__user_id=user_id
    ).exclude(user_id=user_id)

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

'''Choices are: followers, follows, id, related_to, relation, user, user_id'''

@register.simple_tag
def user_likes_or_not(liked_tweet, liker):
    query = Like.objects.filter(liked_tweet=liked_tweet,liker=liker).exists()
    return query
