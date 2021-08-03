from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

app_name = 'user'

urlpatterns = [
    path('login/',obtain_jwt_token,name="login"),
    path('register/',views.UserView.as_view(),name="register"),
    path("details/",views.UserDetail.as_view(),name="user-information"),
    path("charge/",views.Charge.as_view(),name="charge"),
    path("pay/",views.Pay.as_view())
]