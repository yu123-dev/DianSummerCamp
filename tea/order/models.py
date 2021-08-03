from django.db import models
from mytea.models import Tea,Store
from userprofile.models import User

# Create your models here.
#大订单
class Order(models.Model):
    #订单号
    oid = models.CharField(max_length=20)
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name="order")
    store = models.ForeignKey(to=Store,on_delete=models.CASCADE,related_name="order")
    total_price = models.FloatField(default=0)
    #为历史订单或当前订单
    status = models.BooleanField(default=False)
    #已支付或未支付
    paied = models.BooleanField(default=False)
    otime = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('-otime',)#按创建时间排序

    def __str__(self):
        return str(self.oid+":"+str(self.total_price))

#单一商品订单
class SingleOrder(models.Model):
    tea = models.ForeignKey(to=Tea,on_delete=models.CASCADE,related_name="tea")
    Order = models.ForeignKey(to=Order,on_delete=models.CASCADE,related_name="items")
    #加上各种料之后的单价
    sprice = models.FloatField(default=0)
    num = models.IntegerField(default=0)

    def __str__(self):
        return str(self.tea.name+"x"+str(self.num))

#选择题（甜度，冰之类的）
class TeaAdd(models.Model):
    TeaAdd_name = models.CharField(max_length=100)
    TeaAdd_Tea = models.ManyToManyField(to=Tea,related_name='TeaAdd')

    def __str__(self):
        return self.TeaAdd_name

#选项(少冰，标准甜之类的)
class Option(models.Model):
    Option_name = models.CharField(max_length=100)
    Option_price = models.FloatField(default=0)
    Option_TeaAdd = models.ForeignKey(to=TeaAdd,on_delete=models.CASCADE,related_name='Option')
    Option_Single = models.ManyToManyField(to=SingleOrder,related_name='Option')

    def __str__(self):
        return self.Option_name
