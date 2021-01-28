import datetime
import json

from django.contrib import messages
from django.core import serializers
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, CreateView, ListView, DeleteView, DetailView

from catalog.forms.forms import ProductAddForm, ProductFullForm, ImageForm
from catalog.models.models import Category, Product, Tag, Image
from core.forms.forms import SearchForm

from vendors.models import Store


def index(request):
    category = Category.objects.all()
    product = Product.objects.all()
    store = Store.objects.all()
    context = {
        'category': category,
        'catalog': product,
        'store': store,

    }
    return render(request, 'admin/', context)


def categories(request):
    categories = Category.objects.filter(status='True')

    context = {
        'categories': categories,

    }
    return render(request, 'admin/pages/category-admin.html', context)


class AddCategory(CreateView):
    model = Category
    template_name = 'admin/pages/add-category.html'
    fields = '__all__'

    success_url = reverse_lazy('core:categories')


class EditCategory(UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'admin/pages/edit-category.html'
    success_url = reverse_lazy('core:categories')


class DeleteCategory(DeleteView):
    model = Category
    fields = '__all__'
    template_name = 'admin/pages/message/category_confirm_delete.html'
    success_url = reverse_lazy('core:category_admin')

def products_admin(request):
    products = Product.objects.filter(status='True')

    context = {
        'products': products,

    }
    return render(request, 'admin/pages/products-admin.html', context)


class ProductView(ListView):
    template_name = 'admin/pages/products-admin.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.all()


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'admin/pages/product-detail.html'


class ProductCreate(CreateView):
    model = Product
    form_class = ProductAddForm
    #fields = '__all__'
    template_name = 'add-producttest.html'
    # template_name = 'coretest.html'
    success_url = reverse_lazy('core:product')


class ProductUpdate(UpdateView):
    model = Product
    template_name = 'admin/pages/edit-product.html'
    #fields = ['title',]
    success_url = reverse_lazy('core:product')


class ProductDelete(DeleteView):
    model = Category
    # template_name = 'admin/pages/message/category_confirm_delete.html'
    success_url = '/admin/catalog/'

    def get_success_url(self):
        return reverse('core:product')


''''



@login_required  
def movies_create(request):  
     form = MoviesForm(request.POST or None)  
   
     if form.is_valid():  
         movies = form.save(commit=False)  
         movies.user = request.user  
         movies.save()  
         return redirect('CRUD_FBVs:movies_list')  
     return render(request, 'movies_form.html', {'form': form})  
  
'''''


def getNoteResponseData(product_obj, tags, product_created):
    date = datetime.datetime.now().strftime('%B') + " " + datetime.datetime.now().strftime(
        '%d') + ", " + datetime.datetime.now().strftime('%Y')
    product_obj.refresh_from_db()
    response_data = {
        "id": product_obj.id,
        "title": product_obj.title,
        "keywords": product_obj.keywords,
        "price": product_obj.price,
        "tags": tags,
        "last_mod": date,
        "note_created": product_created
    }
    # return JsonResponse(response_data)
    # template_name = 'admin/pages/message/category_confirm_delete.html'
    # success_url = reverse_lazy('core:category_admin')
    return render(product_created, 'admin/pages/category-admin.html')


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


# return render(request,'admin/stores-list.html')


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


def AddProductView(request):
    if request.method == "POST":
        form = ProductFullForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('images')
        if form.is_valid():
            print(request.POST)
            product_created = True
            title = form.cleaned_data['title']
            keywords = form.cleaned_data['keywords']
            description = form.cleaned_data['description']
            thumbnail = form.cleaned_data['thumbnail']
            image1 = form.cleaned_data['image1']
            image2 = form.cleaned_data['image2']
            image3 = form.cleaned_data['image3']
            image4 = form.cleaned_data['image4']
            image5 = form.cleaned_data['image5']
            image6 = form.cleaned_data['image6']
            category = form.cleaned_data['category']
            variant = form.cleaned_data['variant']
            price = form.cleaned_data['price']
            sale_price = form.cleaned_data['sale_price']
            discount = form.cleaned_data['discount']
            amount = form.cleaned_data['amount']
            min_amount = form.cleaned_data['min_amount']
            detail = form.cleaned_data['detail']
            slug = form.cleaned_data['slug']
            status = form.cleaned_data['status']
            product_id = form.cleaned_data['product_id']
            tags = tagsInDic(form.cleaned_data['tags'].strip())
            tags_dic = tags.copy()
            if not product_id:
                print(request)
                product_obj = Product.objects.create(title=title, keywords=keywords, category=category,
                                                     description=description,variant=variant,
                                                     image1=image1, image2=image2, image3=image3, image4=image4,
                                                     image5=image5, image6=image6,
                                                     thumbnail=thumbnail, price=price, sale_price=sale_price,
                                                     discount=discount,
                                                     amount=amount, min_amount=min_amount, detail=detail,
                                                     slug=slug, status=status
                                                     )  # create will create as well as save too in db.
                for k in tags.keys():
                    tag_obj, created = Tag.objects.get_or_create(name=k)
                    product_obj.tags.add(tag_obj)  # it won't add duplicated as stated in django docs
            else:
                # handling all cases of the tags
                print(request)
                product_obj = Product.objects.get(id=product_id)
                for t in product_obj.tags.all():
                    if t.name not in tags_dic:
                        product_obj.tags.remove(t)
                    else:  # deleting pre-existing element so that we could know what's new tags are
                        del tags_dic[t.name]
                for k, v in tags_dic.items():
                    tag_obj, created = Tag.objects.get_or_create(name=k)
                    product_obj.tags.add(tag_obj)
                product_created = False
            for f in files:
                print(request)
                Image.objects.create(product=product_obj, image=f)
            product_obj.category = category
            product_obj.variant=variant
            product_obj.title = title
            product_obj.keywords = keywords
            product_obj.description = description
            product_obj.thumbnail = thumbnail
            product_obj.image1 = image1
            product_obj.image2 = image2
            product_obj.image3 = image3
            product_obj.image4 = image4
            product_obj.image5 = image5
            product_obj.image6 = image6
            product_obj.price = price
            product_obj.sale_price = sale_price
            product_obj.discount = discount
            product_obj.amount = amount
            product_obj.min_amount = min_amount
            product_obj.detail = detail
            product_obj.slug = slug
            product_obj.status = status
            print(request.POST)
            product_obj.save()  # last_modified field won't update on chaning other model field, save() trigger change
            # return reverse('core:catalog')
            return HttpResponseRedirect('/admin/product', product_created)
            # return render(request,template_name='admin/pages/products-admin.html')
            # return getNoteResponseData(product_obj, tags, product_created)
        else:
            print("Form invalid, see below error msg")
            print(request.POST)
            print(form.errors)
            messages.error(request, "Error")
    # if GET method form, or anything wrong then we will create blank form
    else:
        form = ProductFullForm()
    # return HttpResponseRedirect('/')
    return render(request, 'add-product.html', {'form': form})
def EditProductView(request  ):
    if request.method == "POST":
        form = ProductFullForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('images')
        if form.is_valid():
            print(request.POST)
            product_created = True
            title = form.cleaned_data['title']
            keywords = form.cleaned_data['keywords']
            description = form.cleaned_data['description']
            thumbnail = form.cleaned_data['thumbnail']
            image1 = form.cleaned_data['image1']
            image2 = form.cleaned_data['image2']
            image3 = form.cleaned_data['image3']
            image4 = form.cleaned_data['image4']
            image5 = form.cleaned_data['image5']
            image6 = form.cleaned_data['image6']
            category = form.cleaned_data['category']
            price = form.cleaned_data['price']
            sale_price = form.cleaned_data['sale_price']
            discount = form.cleaned_data['discount']
            amount = form.cleaned_data['amount']
            min_amount = form.cleaned_data['min_amount']
            detail = form.cleaned_data['detail']
            slug = form.cleaned_data['slug']
            status = form.cleaned_data['status']
            product_id = form.cleaned_data['product_id']
            tags = tagsInDic(form.cleaned_data['tags'].strip())
            tags_dic = tags.copy()
            if not product_id:
                print(request)
                product_obj = Product.objects.create(title=title, keywords=keywords, category=category,
                                                     description=description,
                                                     image1=image1, image2=image2, image3=image3, image4=image4,
                                                     image5=image5, image6=image6,
                                                     thumbnail=thumbnail, price=price, sale_price=sale_price,
                                                     discount=discount,
                                                     amount=amount, min_amount=min_amount, detail=detail,
                                                     slug=slug, status=status
                                                     )  # create will create as well as save too in db.
                for k in tags.keys():
                    tag_obj, created = Tag.objects.get_or_create(name=k)
                    product_obj.tags.add(tag_obj)  # it won't add duplicated as stated in django docs
            else:
                # handling all cases of the tags
                print(request)
                product_obj = Product.objects.get(id=product_id)
                for t in product_obj.tags.all():
                    if t.name not in tags_dic:
                        product_obj.tags.remove(t)
                    else:  # deleting pre-existing element so that we could know what's new tags are
                        del tags_dic[t.name]
                for k, v in tags_dic.items():
                    tag_obj, created = Tag.objects.get_or_create(name=k)
                    product_obj.tags.add(tag_obj)
                product_created = False
            for f in files:
                print(request)
                Image.objects.create(product=product_obj, image=f)
            product_obj.category = category
            product_obj.title = title
            product_obj.keywords = keywords
            product_obj.description = description
            product_obj.thumbnail = thumbnail
            product_obj.image1 = image1
            product_obj.image2 = image2
            product_obj.image3 = image3
            product_obj.image4 = image4
            product_obj.image5 = image5
            product_obj.image6 = image6
            product_obj.price = price
            product_obj.sale_price = sale_price
            product_obj.discount = discount
            product_obj.amount = amount
            product_obj.min_amount = min_amount
            product_obj.detail = detail
            product_obj.slug = slug
            product_obj.status = status
            print(request.POST)
            product_obj.save()  # last_modified field won't update on chaning other model field, save() trigger change
            # return reverse('core:catalog')
            return HttpResponseRedirect('/admin/product', product_created)
            # return render(request,template_name='admin/pages/products-admin.html')
            # return getNoteResponseData(product_obj, tags, product_created)
        else:
            print("Form invalid, see below error msg")
            print(request.POST)
            print(form.errors)
            messages.error(request, "Error")
    # if GET method form, or anything wrong then we will create blank form
    else:
        form = ProductFullForm()
    # return HttpResponseRedirect('/')
    return render(request, 'edit-product.html', {'form': form})
