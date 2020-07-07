from django.conf.urls import url
from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken,obtain_jwt_token

from day7 import views

urlpatterns = [
    url(r"login/",ObtainJSONWebToken.as_view()),
    url(r"ees/",obtain_jwt_token),
    path('user/',views.Users.as_view()),
    path('logins/',views.Login.as_view()),
    path('computer/',views.Computers.as_view()),
]
