# Create your views here.
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User
from tweetpost.forms import TweetForm
from tweet.models import UserProfile
from tweetpost.models import Tweet



def sign_up(request):
    form = UserCreationForm()
    return render(request, 'user/sign/up.html', {'form': form})


def sign_up_process(request):
    new_user_form = UserCreationForm(request.POST or None)
    if new_user_form.is_valid():
        new_user_form.save()
        return redirect(reverse('sign_up_success'))
    return render(request, 'user/sign/up.html', {'form': new_user_form})


def sign_up_success(request):
    return render(request, 'user/sign/up_success.html')


def sign_in(request):
    form = AuthenticationForm()
    return render(request, 'user/sign/in.html', {'form': form})


def sign_in_process(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('/')
    return render(request, 'user/sign/in.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('/')

def timeline(request):
    if not request.user.is_authenticated():
        return redirect(reverse('sign_up'))

    tweet_form = TweetForm()

    me = request.user.profile
    people_i_follow = UserProfile.objects.filter(followers__follower=me)

    tweets_from_people_i_follow = Tweet.objects.filter(
        tweeter__in=people_i_follow
    ).order_by('-added')

    my_tweets = me.user_tweets.order_by('-added')

    return render(request, 'index.html', {
        'tweet_form': tweet_form,
        'tweets': my_tweets | tweets_from_people_i_follow
    })

def follow(request):
    user_to_follow = User.objects.get(pk=request.GET.get('id'))
    active_user = request.user.profile
    active_user.follow(user_to_follow.profile)
    return HttpResponse('OK')

def unfollow(request):
    user_to_unfollow = User.objects.get(pk=request.GET.get('id'))
    active_user = request.user.profile
    active_user.unfollow(user_to_unfollow.profile)
    return HttpResponse('OK')
