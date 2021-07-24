from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'user'

urlpatterns = [
    path('login/',obtain_jwt_token,name="login"),
    path('register/',views.UserView.as_view()),
]