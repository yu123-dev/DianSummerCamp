from django.urls import path
from . import views

app_name = 'mytea'

urlpatterns = [
    path('tea-list/', views.tea_list.as_view(), name = 'tea-list'),
]