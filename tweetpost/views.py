# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Tweet
from .forms import TweetForm
from .helpers import convert_hashtag_to_link

def tweet(request):
    submitted_tweet_form = TweetForm(request.POST or None)

    if submitted_tweet_form.is_valid():
        tweet_ = submitted_tweet_form.save(commit=False)
        tweet_.content = convert_hashtag_to_link(tweet_.content)
        tweet_.tweeter = request.user.profile
        tweet_.save()
        return redirect(reverse('timeline'))

    return render(request, 'index.html', {
        'tweet_form': submitted_tweet_form,
        'tweets': Tweet.objects.order_by('-added')
    })

def hashtag_search(request):
    hashtag = request.GET.get('h', '')
    tweets = Tweet.objects.filter(content__icontains='#%s' % hashtag)
    return render(request, 'index.html', {
        'tweets': tweets,
        'tweet_form': TweetForm(),
    })
