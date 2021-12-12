from django.urls import path
from . import views

urlpatterns = [
    path('', views.root, name='sign_up'), #root - sign up 
    path('create_new_user', views.create_new_user),
    path('sign_in', views.sign_in, name='sign_in'), #sign in - login
    path('login', views.login),
    path('user', views.user_dash),
    path('poke/<int:id>', views.make_a_poke, name="user_id"),
    path('logout', views.logout),
    #path('poke', views.make_a_poke)
    ]