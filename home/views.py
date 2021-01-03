import datetime
import json
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render
from django.views.generic import  ListView,  DetailView
from catalog.models.models import Category, Product, Tag, Images
from home.forms import SearchForm
from SiteSetting.models import Store


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    store = Store.objects.all()

    setting = Store.objects.get(pk=1)


    products_latest = Product.objects.all().order_by('-id')[:4]  # last 4 products
    products_slider = Product.objects.all().order_by('id')[:4]  # first 4 products
    products_picked = Product.objects.all().order_by('?')[:4]  # Random selected 4 products

    context = {
        'categories': categories,
        'products': products,
        'store': store,
        "setting": setting,
        'products_slider': products_slider,
        'products_latest': products_latest,
        'products_picked': products_picked,
        # 'category':category
    }
    return render(request, 'front/index.html', context)


def categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    # return HttpResponse(1)
    return render(request, 'front/pages/category_list.html', context)


class ProductView(ListView):
    template_name = 'admin/pages/products-admin.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'admin/pages/product-detail.html'


def search(request):
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']  # get form input data
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(
                    title__icontains=query)  # SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()
            context = {'products': products, 'query': query,
                       'category': category}
            return render(request, 'front/pages/search.html', context)

    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title + " > " + rs.category.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

    def to_json(self, objects):
        return serializers.serialize('json', objects)
