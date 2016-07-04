import re

from django.db.models import F
from .models import HashTag

def convert_hashtag_to_link(tweet):
    """
    This function converts hashtags into links and extracts hashtags and saves it in HashTag model
    """
    hashtags = [i for i in tweet.split() if i.startswith('#')]
    for hashtag in hashtags:
        hash_object, created = HashTag.objects.get_or_create(
            tag=hashtag
        )
        hash_object.number = F('number') + 1
        hash_object.save(update_fields=['number'])

    return re.sub('#(\w+)', r'<a href="/tweet/hashtag/?h=\1">#\1</a>', tweet)
