# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Tweet
from .forms import TweetForm
from .helpers import convert_hashtag_to_link

# tweet is posted from tweet_form
# validates the data and then saves to db
# then the hashtag is coverted to link
def tweet(request):
    # data is received from "TweetForm" request via post method
    submitted_tweet_form = TweetForm(request.POST or None)

    # validates the tweeted post data from "submitted_tweet_form"
    if submitted_tweet_form.is_valid():
        # data is stored in "tweet_", commiting false
        tweet_ = submitted_tweet_form.save(commit=False)
        # any hashtags from the tweeted post content will be converted to link
        tweet_.content = convert_hashtag_to_link(tweet_.content)
        # the post 'tweeter' is a 'user' from django "User" model
        # the relation created in "Tweet" model, related name was "profile"
        tweet_.tweeter = request.user.profile
        # Tweet post is saved now
        tweet_.save()
        # redirected to the timeline view
        return redirect(reverse('timeline'))
    # normally the tweet view will show the index view
    # and the data it will send to 'index.html' view
    return render(request, 'index.html', {
        # for this view, "index.html"
        # here the first one one hold the "submitted_tweet_form" data
        # this thing works first, after this, the "if" block abvoe starts it's work
        # next 'tweets' is a query that arranges the posts in order by date
        # ????????????????????????????????????
        'tweet_form': submitted_tweet_form,
        'tweets': Tweet.objects.order_by('-added')
    })

# if any user want to search for a hash tag
def hashtag_search(request):
    hashtag = request.GET.get('h', '')
    tweets = Tweet.objects.filter(content__icontains='#%s' % hashtag)
    return render(request, 'index.html', {
        'tweets': tweets,
        'tweet_form': TweetForm(),
    })
