from django.urls import path
from . import views

app_name = 'mytea'

urlpatterns = [
    path('tea-list/<int:store_id>/', views.tea_list.as_view(), name = 'tea-list'),#奶茶列表
    path("detail/<int:tea_id>/",views.tea_detail.as_view(),name='tea-detail'),#奶茶详情页
    path('stores/',views.store.as_view(), name='store'),#商店列表路由，不想再建一个app了，就放这里了
]