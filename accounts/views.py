from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth.models import User
from django.conf import settings
from .models import Profile     # Your Profile model
from authlib.integrations.django_client import OAuth


# Create your views here.

# Normal User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after register
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# Profile Editing View
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # Change if needed
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})


# Twitter OAuth2 Login & Callback

# Initialize OAuth client
oauth = OAuth()
oauth.register(
    name='twitter',
    client_id=settings.TWITTER_CLIENT_ID,
    client_secret=settings.TWITTER_CLIENT_SECRET,
    authorize_url=settings.TWITTER_AUTHORIZE_URL,
    access_token_url=settings.TWITTER_TOKEN_URL,
    client_kwargs={'scope': settings.TWITTER_SCOPE},
)

# Redirect to Twitter's auth page
def twitter_login(request):
    redirect_uri = request.build_absolute_uri('/auth/twitter/callback/')
    return oauth.twitter.authorize_redirect(request, redirect_uri)

# Handle Twitter callback
def twitter_callback(request):
    token = oauth.twitter.authorize_access_token(request)
    user_info = oauth.twitter.get(settings.TWITTER_USERINFO_URL, token=token).json()

    twitter_id = user_info['data']['id']
    username = f"tw_{twitter_id}"

    user, created = User.objects.get_or_create(username=username)

    # Optional: link token to user's profile here

    login(request, user)
    request.session['twitter_token'] = token

    return redirect('/')
