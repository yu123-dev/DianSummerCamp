from django.contrib import admin
from .models import SingleOrder,Order,TeaAdd,Option
# Register your models here.
admin.site.register(SingleOrder)
admin.site.register(Order)
admin.site.register(TeaAdd)
admin.site.register(Option)