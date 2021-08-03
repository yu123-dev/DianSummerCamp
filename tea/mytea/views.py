from django.shortcuts import HttpResponse
from .models import Store, Tea
from rest_framework.views import APIView
import json

# Create your views here.
#商店列表
class store(APIView):
    def get(self,request):
        stores = Store.objects.all()
        context = {}
        for store in stores:
            #o_num为当前店铺在做的订单数,t_num为奶茶杯数
            o_num = t_num = 0
            #取出所有当前订单
            orders = store.order.filter(status = 0)
            for order in orders:
                o_num+=1
                sorders = order.items.all()
                for sorder in sorders:
                    t_num += sorder.num
            context[store.id] = {"store_id":store.id,"store_name":store.name,"distance":store.distance,'o_num':o_num,'t_num':t_num}
        return HttpResponse(json.dumps(context), content_type="json", charset='utf-8')

#奶茶列表
class tea_list(APIView):
    def get(self,request,store_id):
        store = Store.objects.get(id=store_id)
        teas = store.teas.all()
        context = {"store_id":store.id,"store_name":store.name,"distance":store.distance, "teas":{}}
        for tea in teas:
            context["teas"][tea.id]={"id":tea.id, "name":tea.name, "short_intro":tea.details, "picture":tea.picture}
        return HttpResponse(json.dumps(context), content_type="json", charset='utf-8')

#奶茶详情
class tea_detail(APIView):
    def get(self,request, tea_id):
        tea = Tea.objects.get(id=tea_id)
        #context = {'tea': tea}
        context = {"ID":tea.id,"name":tea.name,"store":tea.store.name, "picture":tea.picture, "details":tea.details, "TeaAdds":{}}
        TeaAdds = tea.TeaAdd.all()
        for TeaAdd in TeaAdds:
            context["TeaAdds"][TeaAdd.id] = {'name':TeaAdd.TeaAdd_name,'options':[]}
            options = TeaAdd.Option.all()
            for option in options:
                context["TeaAdds"][TeaAdd.id]['options'].append(option.Option_name)
        return HttpResponse(json.dumps(context), content_type="json", charset='utf-8')