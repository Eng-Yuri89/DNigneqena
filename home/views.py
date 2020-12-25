from audioop import reverse

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
import json
import datetime
from django.http import JsonResponse
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView, DeleteView
from django.views.generic.base import View

from catalog.models import Category, Product, Image
from home.forms import SearchForm


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    products_latest = Product.objects.all().order_by('-id')[:4]  # last 4 products
    products_slider = Product.objects.all().order_by('id')[:4]  # first 4 products
    products_picked = Product.objects.all().order_by('?')[:4]  # Random selected 4 products
    page = "home"
    context = {
        'categories': categories,
        'products': products,
        'page': page,
        'products_slider': products_slider,
        'products_latest': products_latest,
        'products_picked': products_picked,
        # 'category':category
    }
    return render(request, 'front/index.html', context)


def category_admin(request):
    categories = Category.objects.all()

    context = {
                'categories':categories
    }
    # return HttpResponse(1)
    return render(request, 'admin/pages/category-admin.html', context)

class AddCategory(CreateView):
    model = Category
    template_name = 'admin/pages/add-category.html'
    fields = '__all__'
    #uccess_url =redirect('home:product_admin')
    success_url = reverse_lazy('home:category_admin')



class EditCategory(UpdateView):
    model = Category

    fields = '__all__'
    template_name = 'admin/pages/add-category.html'
    success_url = reverse_lazy('home:category_admin')

class DeleteCategory(DeleteView):
    model = Category
    fields = '__all__'
    template_name = 'admin/pages/message/category_confirm_delete.html'
    success_url = reverse_lazy('home:category_admin')





def products_admin(request):
    category =Category.objects.all()
    products=Product.objects.all()
    context = {'products': products,

               }

    return render(request, 'admin/pages/products-admin.html', context)


def product_admin(request,id,slug):
    query = request.GET.get('q')
    category = Category.objects.all()
    product = Product.objects.get(pk=id)

    context = {'product': product, 'category': category,

               }
    # return HttpResponse('f')
    return render(request, 'admin/pages/product-detail.html', context)


def product_add(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'admin/pages/add-product.html', context)
    if request.method == 'POST':
        title = request.POST.get('title')

        if not title:
            messages.error(request, 'Title is reqired')
            return render(request, 'admin/pages/add-category.html', context)
        parent = request.POST['parent']
        keywords = request.POST['keywords']
        description = request.POST['description']
        image = request.POST['image']
        status = request.POST['status']
        slug = request.POST['slug']

        if not image:
            messages.error(request, 'image is reqiired')
            return request(request, 'admin/pages/add-product.html', context)
        Category.objects.create(title=title, parent=parent, keywords=keywords, description=description,
                                image=image, status=status, slug=slug)
        messages.success(request, 'Category add sucessfuly')

    return render('admin/pages/products-admin')


def product_edit(request,id,slug):

    #return HttpResponse('1')
    products=Product.objects.all()
    product = Product.objects.filter(pk=id)

    context = {
        'product':product,
    }
    if request.method == 'GET':
        return render(request, 'admin/pages/edit-product.html', context)
    if request.method == 'POST':
        title = request.POST.get('title')

        if not title:
            messages.error(request, 'Title is required')
            return render(request, 'admin/pages/edit-product.html', context)
        category = request.POST['category']
        keywords = request.POST['keywords']
        description = request.POST['description']
        image = request.POST.get['image']
        price=request.POST['price']
        n_price=request.POST['n_price']
        discount=request.POST['discount']
        amount=request.POST['amount']
        minamount=request.POST['minamount']
        variant=request.POST['variant']
        detail=request.POST['detail']
        status = request.POST['status']
        slug = request.POST['slug']

        if not category:
            messages.error(request, 'category is required')
            return render(request, 'admin/pages/edit-product.html', context)

        product.title = title
        product.category = category
        product.keywords = keywords
        product.description = description
        product.image = image
        product.price=price
        product.n_price=n_price
        product.discount=discount
        product.amount=amount
        product.minamount=minamount
        product.variant=variant
        product.detail=detail
        product.status = status
        product.slug = slug
        product.save()
        messages.success(request, 'Category updated  successfully')

        return redirect('/admin/product/')



def user_list(request, id, slug):
    # query = request.GET.get('q')

    # usersaaa = UserProfile.objects.all()

    return HttpResponse('h')


# return render(request,'admin/user-list.html')


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
