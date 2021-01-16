from django.db import transaction
from django.forms import formset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, DeleteView, CreateView

#from core.forms.banners_forms import BannersFormSet
#from core.forms.banners_forms import BannersFormSet
from core.models.banners import Banners


class BannerView(TemplateView):
    template_name = "banner/banners-admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Banners'] = Banners.objects.order_by('id')

        return context


class BannerDetailView(DetailView):
    model = Banners
    context_object_name = 'banners'
    template_name = 'banner/banner-detail.html'


class BannerCreate(CreateView):
    model = Banners
    template_name = 'banner/add-banners.html'
    fields =['group','status']
    success_url = reverse_lazy('core:BannerView')
    def get_context_data(self, **kwargs):
        data = super(BannerCreate, self).get_context_data(**kwargs)
        if self.request.POST:

            data['familymembers'] = BannersFormSet(self.request.POST)
        else:
            data['familymembers'] = BannersFormSet
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        familymembers = context['familymembers']
        with transaction.atomic():
            self.object = form.save()

            if familymembers.is_valid():
                familymembers.instance = self.object
                familymembers.save()
        return super(BannerCreate, self).form_valid(form)


class ProfileCreate(CreateView):
    model = Banners
    fields = ['banner_name', 'status']

class CollectionDelete(DeleteView):
    model = Banners
    template_name = 'banner/confirm_delete.html'
    success_url = reverse_lazy('core:BannerView')
