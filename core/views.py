import datetime
import json

from django.core import serializers
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import title
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, DeleteView, DetailView

from catalog.forms.forms import ProductAddForm, ManufacturerAddForm, ImageForm, SingleProductAddForm
from catalog.models.models import Category, Product, Tag, Images
from core.forms import SearchForm





def index(request):
    categories = Category.objects.all()
    product = Product.objects.all()



    products_latest = Product.objects.all().order_by('-id')[:4]  # last 4 products
    products_slider = Product.objects.all().order_by('id')[:4]  # first 4 products
    products_picked = Product.objects.all().order_by('?')[:4]  # Random selected 4 products

    context = {
        'categories': categories,
        'product': product,

        'products_slider': products_slider,
        'products_latest': products_latest,
        'products_picked': products_picked,
    }
    return render(request, 'admin/', context)


def categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        #'setting': setting,

    }
    # return HttpResponse(1)
    return render(request, 'admin/pages/category-admin.html', context)


class AddCategory(CreateView):
    model = Category
    template_name = 'admin/pages/add-category.html'
    fields = '__all__'
    # uccess_url =redirect('core:product_admin')
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
    form = SingleProductAddForm
    template_name = 'admin/pages/add-product.html'
    fields = '__all__'
    success_url = reverse_lazy('core:product')


class ProductUpdate(UpdateView):
    model = Product
    template_name = 'admin/pages/edit-product.html'
    fields = '__all__'
    success_url = reverse_lazy('core:product')


class ProductDelete(DeleteView):
    model = Category
    # template_name = 'admin/pages/message/category_confirm_delete.html'
    success_url = '/admin/product/'

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

def addProductView(request):
    #print(request.POST)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SingleProductAddForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            print(request.POST)
            form.save()
            # redirect to a new URL:

            return HttpResponseRedirect('/admin/product')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProductAddForm()
        print(request.POST)

    return render(request, 'admin/pages/add-product.html', {'form': form})


def sa(request):


    if request.method == 'POST':

        ProductForm = ProductAddForm(request.POST)
        if ProductForm.is_valid():
            ProductForm.save()
            return HttpResponseRedirect('admin/product')
        else:
            print(ProductForm.errors)

    else:
        ProductForm = ProductAddForm()

        return render(request, 'admin/pages/add-product.html',)










def tre(request):

    if request.method == "POST" :
        form = ProductAddForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('images')
        if form.is_valid():
            try:
                form.save()
                return redirect('/admin/product')
            except:
                pass
    else:
        form = ProductAddForm()
    return render(request, 'admin/pages/add-product.html', {'form': form})


def addProdumkctView(request ,):
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=6)
    if request.method == 'POST':
        print(request.POST)
        ProductForm = ProductAddForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())
        print(request.POST)
        if ProductForm.is_valid() and formset.is_valid():
            ProductForm.save()
            for form in formset.cleaned_data:
                image = form['image']
                picture = ImageForm(product=ProductAddForm, image=image)
                picture.save()
                return HttpResponseRedirect('admin/product')
            else:
                print(ProductForm.errors, formset.errors)
    else:
        print(request.POST)
        ProductForm = ProductAddForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'admin/pages/add-product.html', {'ProductForm': ProductForm, 'formset': formset},
                  )



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


# return render(request,'admin/stores-list.html')


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
