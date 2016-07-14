# Create your views here.
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.core.urlresolvers import reverse
from .models import Tweet, Comment, Like
from .forms import TweetForm, CommentForm
from .helpers import convert_hashtag_to_link
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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

def add_comment_to_post(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.tweet = tweet
            comment.save()
            return redirect('timeline')
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('timeline')

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('timeline')

@login_required
def add_like(request):
    if request.method == 'GET':
        ans_id = request.GET['id']
        user = request.user.profile
        liked_tweet = get_object_or_404(Tweet, pk=ans_id)
        is_liked = Like.objects.filter(liked_tweet=ans_id, liker=user).exists()

    #if ans_id:
    if not is_liked:
        # creating instance by sending the Like table fields
        instance, created = Like.objects.get_or_create(liker=user, liked_tweet=liked_tweet)
        ans = Tweet.objects.get(id=(int(ans_id)))
        if ans:
            likes = ans.likes + 1
            ans.likes = likes
            ans.save()
    # returns the likes field of a tweet post
    # return JsonResponse({'like_count':likes})
    return HttpResponse(likes)
    # return render(request, 'index.html', {'likes': likes, 'is_liked': is_liked})

@login_required
def add_unlike(request):
    if request.method == 'GET':
        ans_id = request.GET['id']
        user = request.user.profile
        liked_tweet = get_object_or_404(Tweet, pk=ans_id)

    if ans_id:
        Like.objects.filter(liker=user,liked_tweet=liked_tweet).delete()
        ans = Tweet.objects.get(id=(int(ans_id)))
        if ans:
            likes = ans.likes - 1
            ans.likes = likes
            ans.save()
    # returns the likes field of a tweet post
    return HttpResponse(likes)
    # return JsonResponse({'like_count':likes})
