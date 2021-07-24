from django.shortcuts import render,HttpResponse
from .models import Tea
from rest_framework.views import APIView

# Create your views here.
class tea_list(APIView):
    def get(self,request):
        teas = Tea.objects.all()
        context = {'teas': teas}
        return render(request, 'tea/list.html', context)
