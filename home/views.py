import json

from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from catalog.models import Category, Product, Images
from home.forms import SearchForm


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





def category_admin(request):
    catdata = Category.objects.all()
    products = Product.objects.all()

    context = {'products': products,
               # 'category':category,
               'catdata': catdata}
    #return HttpResponse(1)
    return render(request, 'admin/pages/category.html', context)


def category_products(request):
    catdata = Category.objects.all()
    products = Product.objects.all()

    context = {'products': products,
               # 'category':category,
               'catdata': catdata}
    #return HttpResponse(1)
    return render(request, 'front/pages/category.html', context)


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


def search(request):
    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)

            category = Category.objects.all()
            context = {'products': products, 'query':query,
                       'category': category }
            return render(request, 'front/pages/search.html', context)

    return HttpResponseRedirect('/')

def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title +" > " + rs.category.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


