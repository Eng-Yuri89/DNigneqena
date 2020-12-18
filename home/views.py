from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from catalog.models import Category, Product, Images


def index(request):
    products_latest = Product.objects.all().order_by('-id')[:4]  # last 4 products

    products_slider = Product.objects.all().order_by('id')[:4]  # first 4 products

    products_picked = Product.objects.all().order_by('?')[:4]  # Random selected 4 products



    page = "home"
    context = {
        'page': page,
        'products_slider': products_slider,
        'products_latest': products_latest,
        'products_picked': products_picked,


        # 'category':category
    }
    return render(request, 'front/index.html', context)


def category_products(request, id, slug):
    currentlang = request.LANGUAGE_CODE[0:2]
    catdata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)  # default language

    context = {'products': products,
               # 'category':category,
               'catdata': catdata}
    return render(request, 'front/pages/category-page.html', context)


def user_list(request, id, slug):
    # query = request.GET.get('q')

    # users = UserProfile.objects.all()

    return HttpResponse('h')
# return render(request,'admin/user-list.html')


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
    return render(request,'front/pages/product-page.html',context)
