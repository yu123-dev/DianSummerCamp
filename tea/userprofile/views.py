from rest_framework import generics,permissions
from userprofile.serializers import RegisterSerializer
from rest_framework_jwt.views import obtain_jwt_token

class UserView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    # 注意需要指定permission_classes = []为空列表或者允许所有权限[rest_framework.permissions.AllowAny]
    permission_classes = []

