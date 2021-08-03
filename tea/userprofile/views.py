from django.shortcuts import HttpResponse
from rest_framework import generics
from userprofile.serializers import RegisterSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from django.http import JsonResponse
from tea.tasks import upgrade
from order.models import Order
import datetime
import json

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

#注册
class UserView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    # 注意需要指定permission_classes = []为空列表或者允许所有权限[rest_framework.permissions.AllowAny]
    permission_classes = []

#个人信息
class UserDetail(APIView):
    def get(self,request):
        try :
            user = request.user
            context={
                "user_id":user.id,
                "user_name":user.username,
                "user_phone":user.phone,
                "user_money":user.money,
                "order":{}
            }
            orders = user.order.all()
            for order in orders:
                context["order"]={"订单号":order.oid,"价格":order.total_price,"时间":order.otime.strftime('%Y-%m-%d %H:%M:%S'),"状态":order.status,"商品":{}}
                items = order.items.all()
                for item in items:
                    context["order"]["商品"][item.id]={"tea":item.tea.name,"singleprice":item.sprice,"num":item.num,"options":[option.Option_name for option in item.Option.all()]}
            return HttpResponse(json.dumps(context), content_type="json")
        except:
            return JsonResponse({'msg':'请先登录'})
#充值
class Charge(APIView):
    def post(self,request):
        num = request.data.get("charge")
        try: 
            user = request.user
            user.money += float(num)
            user.save()
            print('当前余额{0}'.format(user.money))
            return JsonResponse({'msg':'当前余额{0}'.format(user.money)})
        except:
            return JsonResponse({'msg':'请先登录'})

#支付
class Pay(APIView):
    def post(self,request):
        try:
            user = request.user
            num = request.data.get('pay')#支付金额
            oid = request.data.get('oid')#需支付的订单号
            order = Order.objects.get(oid=oid)
            if num != order.total_price:
                return JsonResponse({'msg':'金额错误'})
            if user.money >= float(num):#如果钱够就支付
                user.money -= float(num)
                user.save()
                order.paied = True#改变订单支付状态
                order.save()
                upgrade.delay(order.pk)#支付后将订单放入任务队列，排队等待，任务队列使用了celery的异步任务处理
                return JsonResponse({'msg':'支付成功'},json_dumps_params={'ensure_ascii':False})
            else:
                return JsonResponse({'msg':'请先充值'})
        except:
            return JsonResponse({'msg':'请先登录'})