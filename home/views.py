import datetime
import json
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from haystack import indexes
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery, Exact, Clean
from catalog.models.models import Category, Product, Tag, Image
from core.models.banners import Banners

from home.forms import SearchForm
from vendors.models import Store


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    store = Store.objects.all()
    banner = Banners.objects.all()

    top_collection = Product.objects.all().order_by('-id')[:8]  # last 4 products
    products_first = Product.objects.all().order_by('id')[:8]  # first 4 products
    new_products = Product.objects.all().order_by('-id')[:2]  # New Products
    new_sale_products = Product.objects.all().order_by('-id')[:2]  # New Products
    new_random_products = Product.objects.all().order_by('id', 'update_at')[:4]  # New Products
    featured_products = Product.objects.all().order_by('id')[:8]  # Featured Products
    best_products = Product.objects.all().order_by('?')[:8]  # Best Sellers

    context = {
        'categories': categories,
        'products': products,
        'store': store,
        'banner': banner,
        'top_collection': top_collection,
        'products_first': products_first,
        'new_products': new_products,
        'new_sale_products': new_sale_products,
        'new_random_products': new_random_products,
        'featured_products': featured_products,
        'best_products': best_products,
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
    template_name = 'product-no-sidebar.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['productlest'] = Product.objects.all()
        context['prodtag'] = Product.category
        return context


def search(request):
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']  # get form input data
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(
                    title__icontains=query)  # SELECT * FROM catalog WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)

            category = Category.objects.all()
            context = {'products': products, 'query': query,
                       'category': category}
            return render(request, 'front/pages/search.html', context)

    return render(request, 'front/pages/search.html')


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


def search_titles(request):
    product_search = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text', ''))
    #sqs = SearchQuerySet().filter(content='foo').load_all()
    sqs = SearchQuerySet().filter(content='foo').stats('price')

    print(request.POST)

    return render(request,'search/search.html', {'product_search': product_search , 'sqs':sqs})


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')
