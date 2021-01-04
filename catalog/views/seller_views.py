import os
from mimetypes import guess_type
from django.conf import settings
from wsgiref.util import FileWrapper

from django.db.models import Q, Avg, Count
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import View

from DNigne.mixins import AjaxRequiredMixin, SubmitBtnMixin, MultiSlugMixin, LoginRequiredMixin
from analytics.models import TagView
from catalog.forms.seller_forms import ProductModelForm
from catalog.mixins import ProductManagerMixin
from catalog.models.seller_models import SellerProduct, ProductRating, MyProducts
from tags.models import Tag
from vendors.mixins import SellerAccountMixin


class ProductRatingAjaxView(AjaxRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # if request.is_ajax():
        # raise Http404
        if not request.user.is_authenticated():
            return JsonResponse({}, status=401)
        # credit card required **

        user = request.user
        product_id = request.POST.get("product_id")
        rating_value = request.POST.get("rating_value")
        exists = SellerProduct.objects.filter(id=product_id).exists()
        if not exists:
            return JsonResponse({}, status=404)

        try:
            product_obj = SellerProduct.object.get(id=product_id)
        except:
            product_obj = SellerProduct.objects.filter(id=product_id).first()

        rating_obj, rating_obj_created = ProductRating.objects.get_or_create(
            user=user,
            product = product_obj
        )

        try:
            rating_obj = ProductRating.objects.get(user=user, product=product_obj)
        except ProductRating.MultipleObjectsReturned:
            rating_obj = ProductRating.objects.filter(user=user, product=product_obj).first()
        except:
            rating_obj = ProductRating()
            rating_obj.user = user
            rating_obj.product = product_obj
        rating_obj.rating = int(rating_value)
        myproducts = user.myproducts.products.all()
        if product_obj in myproducts:
            rating_obj.verified = True
        rating_obj.save()

        data = {
			"success": True
  		}
        return JsonResponse(data)

class ProductCreateView(SellerAccountMixin, SubmitBtnMixin, CreateView):
    model = SellerProduct
    template_name = "form.html"
    form_class = ProductModelForm
    submit_btn = "Add SellerProduct"

    def form_valid(self, form):
        seller = self.get_account()
        form.instance.seller = seller
        valid_data = super(ProductCreateView, self).form_valid(form)
        tags = form.cleaned_data.get("tags")
        if tags:
            tags_list = tags.split(",")

            for tag in tags_list:
                if not tag == " ":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.products.add(form.instance)


        return valid_data

class ProductUpdateView(ProductManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
    model = SellerProduct
    template_name = "form.html"
    form_class = ProductModelForm
    submit_btn = "Update SellerProduct"

    def get_initial(self):
        initial = super(ProductUpdateView, self).get_initial()

        tags = self.get_object().tag_set.all()
        initial["tags"] = ", ".join([x.title for x in tags])
        """
        tag_list = []
        for x in tags:
            tag_list.append(x.title)
        """
        return initial

    def form_valid(self, form):
        valid_data = super(ProductUpdateView, self).form_valid(form)
        tags = form.cleaned_data.get("tags")
        obj = self.get_object()
        obj.tag_set.clear()
        if tags:
            tags_list = tags.split(",")

            for tag in tags_list:
                if not tag == " ":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.products.add(self.get_object())
        return valid_data


class ProductDetailView(MultiSlugMixin, DetailView):
    model = SellerProduct

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        tags = obj.tag_set.all()
        rating_avg = obj.productrating_set.aggregate(Avg("rating"), Count("rating"))
        context["rating_avg"] = rating_avg
        if self.request.user.is_authenticated():
            rating_obj = ProductRating.objects.filter(user=self.request.user, product=obj)
            if rating_obj.exists():
                context['my_rating'] = rating_obj.first().rating
            for tag in tags:
                new_view = TagView.objects.add_count(self.request.user.id, tag)
        return context

class ProductDownloadView(MultiSlugMixin, DetailView):
    model = SellerProduct

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj in request.user.myproducts.products.all():
            filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
            guessed_type = guess_type(filepath)[0]
            wrapper = FileWrapper(filepath)
            mimetype = 'application/force-download'
            if guessed_type:
                mimetype = guessed_type
            response = HttpResponse(wrapper, content_type='mimetype')

            if not request.GET.get("preview"):
                response["Content-Disposition"] = "attachment; filename=%s" %(obj.media.name)

            response["X-SendFile"] = str(obj.media.name)
            return response
        else:
            raise Http404

class SellerProductListView(SellerAccountMixin, ListView):
    model = SellerProduct
    template_name = "sellers/product_list_view.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(SellerProductListView, self).get_queryset(**kwargs)
        qs = qs.filter(seller=self.get_account())
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)
            ).order_by("title")
        return qs

class VendorListView(ListView):
    model = SellerProduct
    template_name = "products/product_list.html"

    def get_object(self):
        username = self.kwargs.get("vendor_name")
        seller = get_object_or_404(SellerAccount, user__name=username)
        return seller

    def get_context_data(self, *args, **kwargs):
        context = super(VendorListView, self).get_context_data(*args, **kwargs)
        context["vendor_name"] = str(self.get_object().user.username)
        return context

    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get("vendor_name")
        seller = get_object_or_404(SellerAccount, user__name=username)
        qs = super(VendorListView, self).get_queryset(**kwargs).filter(seller=seller)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)
            ).order_by("title")
        return qs

class ProductListView(ListView):
    model = SellerProduct

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(**kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)
            ).order_by("title")
        return qs

class UserLibraryListView(LoginRequiredMixin, ListView):
    model = MyProducts
    template_name = "products/library_list.html"

    def get_queryset(self, *args, **kwargs):
        obj = MyProducts.objects.get_or_create(user=self.request.user)[0]
        qs = obj.products.all()
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)
            ).order_by("title")
        return qs

def create_view(request):
    # Form
    form = ProductModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():

        instance = form.save(commit=False)
        instance.sale_price = instance.price
        instance.save()
    template = "form.html"
    context = {
        "form": form,
        "submit_btn": "Create SellerProduct"
    }
    return render(request, template, context)

def update_view(request, object_id=None):
    product = get_object_or_404(SellerProduct, id=object_id)
    forms = ProductModelForm(request.POST or None, instance=product)
    if forms.is_valid():
        instance = forms.save(commit=False)
        # instance.sale_price = instance.price
        instance.save()
    template = "form.html"
    context = {
            "object": product,
            "form": forms,
            "submit_btn": "Update SellerProduct"
        }
    return render(request, template, context)

def detail_slug_view(request, slug=None):
    product = SellerProduct.objects.get(slug=slug)
    try:
        product = get_object_or_404(SellerProduct, slug=slug)
    except SellerProduct.MultipleObjectsReturned:
        product = SellerProduct.objects.filter(slug=slug).order_by("-title").first()
    template = "detail_view.html"
    context = {
            "object": product
        }
    return render(request, template, context)

def detail_view(request, object_id=None):
    product = get_object_or_404(SellerProduct, id=object_id)
    template = "detail_view.html"
    context = {
            "object": product
        }
    return render(request, template, context)

def list_view(request):

    queryset = SellerProduct.objects.all()
    template = "list_view.html"
    context = {
        "queryset": queryset
    }
    return render(request, template, context)
