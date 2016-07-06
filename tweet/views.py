# importing the dependencies
from django.shortcuts import render, redirect,get_object_or_404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# two model classes need to import first to use them
from tweet.models import UserProfile
from tweetpost.forms import TweetForm
from tweetpost.models import Tweet
# for authentication provided by django
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# sign up view for new users, using the django UserCreationForm
def sign_up(request):
    form = UserCreationForm()
    # returns the UserCreationForm
    return render(request, 'user/sign/up.html', {'form': form})

# defines and validates the sign up process for a new user
# receives the data from the UserCreationForm via post method
# if the data is valid then this method does the entry to db and redirects to sign_up_success
# otherwise stays in the same page, the sign_up page
def sign_up_process(request):
    new_user_form = UserCreationForm(request.POST or None)
    if new_user_form.is_valid():
        new_user_form.save()
        return redirect(reverse('sign_up_success'))
    # this normally returns the containing data from new_user_form
    return render(request, 'user/sign/up.html', {'form': new_user_form})

# after the validation of new_user_form, this page will arrive as success
def sign_up_success(request):
    return render(request, 'user/sign/up_success.html')

# defines the user sign in page
def sign_in(request):
    form = AuthenticationForm()
    return render(request, 'user/sign/in.html', {'form': form})

# defines the users sign in process via receiving the data from AuthenticationForm
# same as sign_up_process
# if the credentials found in db, then the user is allowed to login
def sign_in_process(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        # this login function is provided by django
        login(request, form.get_user())
        return redirect('/')
    # this normally returns the containing data from the sign in form
    return render(request, 'user/sign/in.html', {'form': form})

# django provided logout function
def log_out(request):
    logout(request)
    return redirect('/')

# the ajax method from the base.html is passing the user data(id) to follow
# this method will store both the user "who requested to follow" and "the user to follow"
def follow(request):
    # the user to follow
    user_to_follow = User.objects.get(pk=request.GET.get('id'))
    # this takes the user from the UserProfile who has requested to follow another user
    active_user = request.user.profile # here profile is the "related_name" for UserProfile model's user field
    # this will call the UserProfile's "follow" method passing the "user_to_follow" value
    active_user.follow(user_to_follow.profile)
    return HttpResponse('OK')

# custom method that unfollows a user via getting the specific "pk"
def unfollow(request, pk):
    user_to_unfollow = User.objects.get(pk=pk)
    active_user = request.user.profile
    # this will call the UserProfile's "unfollow" method passing the "user_to_unfollow" value
    active_user.unfollow(user_to_unfollow.profile)
    return redirect('/')

# the main page where user can tweet a post, follow users
def timeline(request):
    if not request.user.is_authenticated():
        return redirect(reverse('sign_up'))
    # the tweet form to submit a post
    tweet_form = TweetForm()
    # the user
    me = request.user.profile
    # the query to get the post from the following users
    people_i_follow = UserProfile.objects.filter(followers__follower=me)
    tweets_from_people_i_follow = Tweet.objects.filter(
        tweeter__in=people_i_follow
    ).order_by('-added')
    # query to retrieve the user posts
    # the line defines:
    # my_tweets = request.user.profile.user_tweets.order_by('-added')
    my_tweets = me.user_tweets.order_by('-added')
    return render(request, 'index.html', {
        'tweet_form': tweet_form,
        'tweets': my_tweets | tweets_from_people_i_follow
    })

# a list page for the following persons list
def following_list(request):
    if not request.user.is_authenticated():
        return redirect(reverse('sign_up'))
    # the user
    me = request.user.profile
    # remember the related_name term, they are used here
    # a query that shows the persons the user is following
    people_i_follow = UserProfile.objects.filter(followers__follower=me)
    return render(request, 'following_list.html', {
        'people_i_follow': people_i_follow
        })

# a list page for the follower persons list
def follower_list(request):
    if not request.user.is_authenticated():
        return redirect(reverse('sign_up'))
    # the user
    me = request.user.profile
    # a query that shows the persons who are following the user
    people_who_following_me = UserProfile.objects.filter(follows__is_followed=me)

    return render(request, 'follower_list.html', {
        'people_who_following_me' : people_who_following_me
        })

# remember, "pk" is passed from the url that is being called for the current view
# each of the profile pages are getting the exact profile via "pk"
# simple profile page view
def profile(request, pk):
    if not request.user.is_authenticated():
        return redirect(reverse('sign_up'))
    prof = get_object_or_404(UserProfile, pk=pk)
    return render(request, 'profile.html', {'prof': prof})

# following profiles
def following_profile(request, pk):
    if not request.user.is_authenticated():
        return redirect(reverse('sign_up'))
    prof = get_object_or_404(UserProfile, pk=pk)
    return render(request, 'following_profile.html', {'prof': prof})

# follower profile
def follower_profile(request, pk):
    if not request.user.is_authenticated():
        return redirect(reverse('sign_up'))
    prof = get_object_or_404(UserProfile, pk=pk)
    return render(request, 'follower_profile.html', {'prof': prof})
