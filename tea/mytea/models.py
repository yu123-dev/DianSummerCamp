from django.db import models


# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=100)
    distance = models.FloatField()

    def __str__(self):
        return self.name

class Tea(models.Model):
    #和店铺关联
    store = models.ForeignKey("Store", on_delete=models.CASCADE,related_name="teas")
    name = models.CharField(max_length=100)
    price = models.FloatField()
    details = models.TextField()
    #status表示是否有货，0为没有，1为有
    status = models.IntegerField(default=1)
    #本地图片地址，服务器上用的ImageField
    picture = models.CharField(max_length=100)

    def __str__(self):
        return self.name