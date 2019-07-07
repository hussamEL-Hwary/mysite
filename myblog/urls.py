from django.urls import path, include
from . import views


app_name = 'blog'

urlpatterns = [
    path("", views.homepage, name='homepage'),
    path("register/", views.register, name='register'),
    path("logout", views.logout_user, name='logout'),
    path("login/", views.login_user, name='login'),
    path("<slug>", views.single_slug, name='sigle_slug'),
]   