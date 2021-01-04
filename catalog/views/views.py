from django.http import HttpResponse, request
from django.shortcuts import render, redirect

# Create your views here.




from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models.models import Category, Product, Images



def index(request):

    catdata = Category.objects.all()
    product = Product.objects.all
    page = "home"
    context = {
        'page': page,

        'catdata':catdata,
        'product':product,
    }
    return render(request, 'admin/index.html', context)


def sidebar(request):

    catdata = Category.objects.all()
    page = "home"
    context = {
        'page': page,

        'catdata':catdata
    }
    return render(request, 'admin/sidebar.html', context)


def category_list(request):
    catdata = Category.objects.all()
    context = {
               # 'category':category,
               'catdata': catdata}
    #return HttpResponse(1)
    return render(request, 'front/pages/category_list.html', context)


def product_list(request):
    catdata = Category.objects.all()
    products = Product.objects.all()

    context = {'products': products,
               # 'category':category,
               'catdata': catdata}
    #return HttpResponse(1)
    return render(request, 'admin/pages/category-admin.html', context)


def user_list(request, id, slug):
    # query = request.GET.get('q')

    # usersaaa = UserProfile.objects.all()

    return HttpResponse('h')
# return render(request,'admin/stores-list.html')


def product_detail(request,id,slug):
    query = request.GET.get('q')
    # >>>>>>>>>>>>>>>> M U L T I   L A N G U G A E >>>>>> START

    category = Category.objects.all()

    product = Product.objects.get(pk=id)

    images = Images.objects.filter(product_id=id)
    paginator = Paginator(images, 1)  # Show 25 contacts per page.

    context = {'product': product,'category': category,
               'images': images,"paginator":paginator
               }
    #return HttpResponse('f')
    return render(request, 'front/pages/product-page.html', context)





class CatList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'admin/pages/category-admin.html'

    def get(self, request):
        queryset = Category.objects.all()
        return Response({'categories': queryset})




