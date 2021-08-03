from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Option, Order,SingleOrder
from mytea.models import Store,Tea

# Create your views here.
class order(APIView):
    #GET方法得到订单的列表，POST生成订单
    def get(self,request):
        try:
            user = request.user
            context = {'当前订单':{},'历史订单':{}}
            #取出当前用户所有历史订单和当前订单（不包括未支付订单）
            pre_orders = Order.objects.filter(status = 1,user = user,paied = 1)
            now_orders = Order.objects.filter(status = 0,user = user,paied = 1)
            #序列化历史订单的所有信息
            for pre_order in pre_orders:
                context['历史订单'][pre_order.id] = {'订单号':pre_order.oid, '总价':pre_order.total_price,"时间":pre_order.otime.strftime('%Y-%m-%d %H:%M:%S'),"商品":{}}
                items = pre_order.items.all()
                for item in items:
                    context['历史订单'][pre_order.id]["商品"][item.id]={"tea":item.tea.name,"singleprice":item.sprice,"num":item.num,"options":[option.Option_name for option in item.Option.all()]}
            #序列化当前订单的所有信息，比历史订单多了一个排队情况
            for now_order in now_orders:
                store = now_order.store
                o_num = t_num = 0
                orders = store.order.filter(status = 0,user = user)
                for order in orders:
                    o_num+=1
                    sorders = order.items.all()
                    for sorder in sorders:
                        t_num += sorder.num
                context['当前订单'][now_order.id] = {'订单号':now_order.oid, '总价':now_order.total_price,"时间":now_order.otime.strftime('%Y-%m-%d %H:%M:%S'),"商品":{},'进度':"{0}单/{1}杯".format(o_num,t_num)}
                items = now_order.items.all()
                for item in items:
                    context['当前订单'][now_order.id]["商品"][item.id]={"tea":item.tea.name,"singleprice":item.sprice,"num":item.num,"options":[option.Option_name for option in item.Option.all()]}
            return JsonResponse(context,json_dumps_params={'ensure_ascii':False})
        except:
            return JsonResponse({'msg':'请先登录'},json_dumps_params={'ensure_ascii':False})

    #post方法生成订单
    def post(self,request):
        '''
            context = {
                'store':1,
                'total_price':40,
                'items':[
                    {
                        'tea':1,
                        'num':2,
                        'options':["少冰"]
                    }
                ]
            }
        '''
        try:
            #先生成大订单，即最终的订单
            user = request.user
            store = Store.objects.get(pk = request.data.get('store'))
            total_price = request.data.get('total_price')
            order = Order()
            order.user = user
            order.store = store
            order.total_price = total_price
            order.save()
            order.oid = str(user.pk) + order.otime.strftime('%Y%m%d%H%M%S')
            #对于每种奶茶分别生成小订单，并关联上各自的选项（少冰，少糖之类的）
            items = request.data.get('items')
            for item in items:
                sorder = SingleOrder()
                sorder.tea = Tea.objects.get(pk=item['tea'])
                sorder.Order = order
                sorder.num = item['num']
                sorder.save()
                for option in item['options']:
                    opt = Option.objects.get(Option_name=option)
                    opt.Option_Single.add(sorder)
                    sorder.sprice += opt.Option_price
                sorder.Order = order
                sorder.sprice += sorder.tea.price
                sorder.save()
            order.save()
            return JsonResponse({'msg':'订单创立成功','oid':order.oid},json_dumps_params={'ensure_ascii':False})
        except:
            return JsonResponse({'msg':'请先登录'},json_dumps_params={'ensure_ascii':False})
