from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),

    # Twitter OAuth 2.0
    path('login/twitter/', views.twitter_login, name='twitter_login'),
    path('auth/twitter/callback/', views.twitter_callback, name='twitter_callback'),
]
