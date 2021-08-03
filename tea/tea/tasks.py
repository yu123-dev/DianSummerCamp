from .celery import app
from order import models
from mytea.models import Store
import time

@app.task 
def upgrade(pk):#计算出订单中的奶茶杯数，以一杯奶茶需要1min来排队
    now_order = models.Order.objects.get(pk=pk)
    now_order.status = True
    sorders = now_order.items.all()
    num = 0
    for sorder in sorders:
        num += sorder.num
    time.sleep(60*num)#阻塞任务队列，达到排队效果
    now_order.save()