from django.test import TestCase

# Create your tests here.

"""""

class ProductView(ListView):
    model = SellerProduct
    template_name = 'admin/pages/products-admin.html'
    paginate_by = 10


class ProductDetailView(DetailView):
    model = SellerProduct
    template_name = 'admin/pages/banner-detail.html'


class ProductCreateView(CreateView):
    model = SellerProduct
    template_name = 'admin/pages/add-product.html'
    fields = '__all__'


def products_admin(request):
    category = Category.objects.all()
    products = SellerProduct.objects.all()
    context = {'products': products,

               }

    return render(request, 'admin/pages/products-admin.html', context)


def product_admin(request, id, slug):
    query = request.GET.get('q')
    category = Category.objects.all()
    product = SellerProduct.objects.get(pk=id)

    context = {'product': product, 'category': category,

               }
    # return HttpResponse('f')
    return render(request, 'admin/pages/banner-detail.html', context)


def create(request):
    if request.method == 'POST':
        form = ProductAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/product')
    form = ProductAddForm()
    return render(request, 'admin/pages/add-product.html', {'form': form})


def edit(request, pk, template_name='admin/pages/edit-product'):
    product = get_object_or_404(SellerProduct, pk=pk)
    form = ProductAddForm(request.POST or None, instance=title)
    if form.is_valid():
        form.save()
        return redirect('/admin/products')
    return render(request, template_name, {'form': form})


def delete(request, pk, template_name='crudapp/confirm_delete.html'):
    product = get_object_or_404(SellerProduct, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('/admin')
    return render(request, template_name, {'object': product})


def product_edit(request, id, slug):
    # return HttpResponse('1')
    products = SellerProduct.objects.all()
    product = SellerProduct.objects.filter(pk=id)

    context = {
        'product': product,
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
        price = request.POST['price']
        n_price = request.POST['n_price']
        discount = request.POST['discount']
        amount = request.POST['amount']
        minamount = request.POST['minamount']
        variant = request.POST['variant']
        detail = request.POST['detail']
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
        product.price = price
        product.n_price = n_price
        product.discount = discount
        product.amount = amount
        product.minamount = minamount
        product.variant = variant
        product.detail = detail
        product.status = status
        product.slug = slug
        product.save()
        messages.success(request, 'Category updated  successfully')

        return redirect('/admin/product/')
        
        
        
        
        
        
        
        
        
        from urllib import request

from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput, Textarea

from catalog.models import Category, SellerProduct, ImageAlbum, Manufacturer


class CategoryAddForm(forms.ModelForm):
    title = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Category
        fields = '__all__'



class ProductAddForm(forms.ModelForm):
    class Meta:
        model = SellerProduct
        fields = '__all__'

class ProductAddFormm(forms.ModelForm):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    category = forms.ModelChoiceField(queryset=Category.objects.filter(title='title'),empty_label="Chose One")  # many to one relation with Category
    title = forms.CharField()
    keywords = forms.CharField()
    description = forms.Textarea()
    m_image = forms.ImageField()
    price = forms.DecimalField()
    n_price = forms.DecimalField()
    discount = forms.DecimalField()
    amount = forms.IntegerField()
    min_amount = forms.IntegerField()
    variant = forms.ChoiceField(choices=VARIANTS)
    slug = forms.SlugField()
    status = forms.ChoiceField(choices=STATUS)
    class Meta:
        model = SellerProduct
        fields = ('category','title','keywords','description','m_image','price','n_price','discount','amount','min_amount'
                  ,'variant','slug','status')


class ManufacturerAddForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'




def addProductView(request):
    if request.method == "POST":
        contributeForm = ProductFullForm(request.POST)

        if contributeForm.is_valid():
            post = contributeForm.save(commit=False)
            try:
                post.save()
                return redirect('/admin/product')
            except:
                pass
        else:
            # this should be include if form validate failed
            return render(request, 'admin/pages/add-product.html', {'contributeForm': contributeForm})
        elif request.method == "GET":
        category = Category.objects.all()
        contributeForm = ProductFullForm()
        context = {'contributeForm': contributeForm
            , 'category': category}
        # return render(request, 'index.html', context) <-- why do you have this here?
        return render(request, 'admin/pages/add-product.html', context)


"""
