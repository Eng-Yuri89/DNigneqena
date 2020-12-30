import datetime
import json

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import title
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, DeleteView, DetailView

from catalog.forms import ProductAddForm, ManufacturerAddForm, ProductFullForm
from catalog.models import Category, Product, Tag, Image
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


def categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    # return HttpResponse(1)
    return render(request, 'admin/pages/category-admin.html', context)


class AddCategory(CreateView):
    model = Category
    template_name = 'admin/pages/add-category.html'
    fields = '__all__'
    # uccess_url =redirect('home:product_admin')
    success_url = reverse_lazy('home:category')


class EditCategory(UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'admin/pages/edit-category.html'
    success_url = reverse_lazy('home:category')


class DeleteCategory(DeleteView):
    model = Category
    fields = '__all__'
    template_name = 'admin/pages/message/category_confirm_delete.html'
    success_url = reverse_lazy('home:category_admin')


class ProductView(ListView):
    template_name = 'admin/pages/products-admin.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'admin/pages/product-detail.html'


class ProductCreate(CreateView):
    model = Product
    template_name = 'admin/pages/add-product.html'
    fields = '__all__'
    success_url = reverse_lazy('home:product')


class ProductUpdate(UpdateView):
    model = Product
    template_name = 'admin/pages/edit-product.html'
    fields = '__all__'
    success_url = reverse_lazy('home:product')


class ProductDelete(DeleteView):
    model = Category
    # template_name = 'admin/pages/message/category_confirm_delete.html'
    success_url = '/admin/product/'

    def get_success_url(self):
        return reverse('home:product')


def fds(request):
    if request.method == "POST":
        form = ProductAddForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/admin/product')
            except:
                pass
    else:
        form = ProductAddForm()
    return render(request, 'admin/pages/add-product.html', {'form': form})


def addProductView(request):
    category = Category.objects.all()
    product = Product.objects.all()
    form = ProductFullForm()
    context = {'category': category,
               'product':product,
               'form':form
               }
    print(request.POST)


    return render(request, 'admin/pages/add-product.html',context)


def tre(request):
    if request.method == "POST":
        form = ProductFullForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('images')
        if form.is_valid():
            product_created = True
            title = form.cleaned_data['title']
            product_id = form.cleaned_data['product_id']
            keywords = form.cleaned_data['keywords']
            tags = tagsInDic(form.cleaned_data['tags'].strip())
            tags_dic = tags.copy()
            if not product_id:
                note_obj = Product.objects.create(title=title)  # create will create as well as save too in db.
                for k in tags.keys():
                    tag_obj, created = Tag.objects.get_or_create(name=k)
                    note_obj.tags.add(tag_obj)  # it won't add duplicated as stated in django docs
            else:
                # handling all cases of the tags
                product_obj = Product.objects.get(id=product_id)
                for t in product_obj.tags.all():
                    if t.name not in tags_dic:
                        product_obj.tags.remove(t)
                    else:  # deleting pre-existing element so that we could know what's new tags are
                        del tags_dic[t.name]
                for k, v in tags_dic.items():
                    tag_obj, created = Tag.objects.get_or_create(name=k)
                    product_obj.tags.add(tag_obj)
                note_created = False
            for f in files:
                Image.objects.create(note=product_obj, image=f)
            product_obj.title = title

            product_obj.save()  # last_modified field won't update on chaning other model field, save() trigger change
            return getNoteResponseData(product_obj, tags, product_created)
        else:
            print("Form invalid, see below error msg")
            print(form.errors)
    # if GET method form, or anything wrong then we will create blank form
    else:
        form = ProductFullForm()
    return render(request, 'admin/pages/add-product.html')


def getNoteResponseData(product_obj, tags, product_created):
    date = datetime.datetime.now().strftime('%B') + " " + datetime.datetime.now().strftime(
        '%d') + ", " + datetime.datetime.now().strftime('%Y')
    product_obj.refresh_from_db()
    response_data = {
        "id": product_obj.id,
        "title": product_obj.title,
        "text": product_obj.text,
        "tags": tags,
        "last_mod": date,
        "note_created": product_created
    }
    return JsonResponse(response_data)


def tagsInDic(tags):
    """Convert comma separated tags into dictionary"""
    last_ind = 0
    res = {}
    for i, c in enumerate(tags):
        if c == ',':
            res[tags[last_ind:i]] = 1
            last_ind = i + 1
    res[tags[last_ind:]] = 1
    return res


##################################################
#
#
#
#################################################
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
