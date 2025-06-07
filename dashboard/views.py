import requests
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Tweet
from .forms import TweetForm

# Create your views here.
def home(request):
    return render(request, 'home.html')


@login_required
def fetch_tweets(request):
    token = request.session.get('twitter_token')
    if not token:
        return render(request, 'dashboard/no_token.html')  # or redirect to login

    headers = {
        'Authorization': f"Bearer {token['access_token']}"
    }

    # Twitter API v2 - get recent tweets from user's timeline
    url = "https://api.twitter.com/2/users/me/tweets"

    response = requests.get(url, headers=headers)
    data = response.json()

    tweets = data.get('data', [])
    for tweet in tweets:
        Tweet.objects.get_or_create(
            user=request.user,
            tweet_id=tweet['id'],
            defaults={
                'text': tweet['text'],
                'created_at': tweet['created_at']
            }
        )

    return render(request, 'dashboard/tweets.html', {'tweets': Tweet.objects.filter(user=request.user)})

@login_required
def post_tweet(request):
    token = request.session.get('twitter_token')
    if not token:
        return redirect('fetch_tweets')

    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet_text = form.cleaned_data['text']

            headers = {
                'Authorization': f"Bearer {token['access_token']}",
                'Content-Type': 'application/json'
            }

            payload = {
                'text': tweet_text
            }

            url = "https://api.twitter.com/2/tweets"
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 201 or response.status_code == 200:
                return redirect('fetch_tweets')
            else:
                return render(request, 'dashboard/post_failed.html', {
                    'error': response.json()
                })
    else:
        form = TweetForm()

    return render(request, 'dashboard/post_tweet.html', {'form': form})
