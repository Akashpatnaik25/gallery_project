from django.urls import path
from user.views import login_api, login_page, signup_api,signup_page


urlpatterns = [

path('',login_page,name="login_page"),
path('login',login_api,name="login_api"),
path('signup-page/', signup_page, name="signup"),
path('signup',signup_api,name="signup_api"),


]