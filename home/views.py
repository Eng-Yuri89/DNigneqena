from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.




def index(request):
    page = "home"
    context = {
               'page': page,
               }
    #return HttpResponse("lang")
    return render(request, 'front/index.html')