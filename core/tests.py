from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import redirect

from core.forms.banners_forms import BannerAddForm, render
from core.models.banners import Banners


def banner_create(request):
    qs = Banners.objects.none()
    BannersFormSet = modelformset_factory(Banners, form=BannerAddForm,exclude=['group','status'], extra=1,can_delete=True)

    if request.method == 'POST':
        banner_form = BannerAddForm(request.POST, prefix='banner')

        formset = BannersFormSet(request.POST ,request.FILES)

        if formset.is_valid() and banner_form.is_valid():
            # Generate a workday object
            banner = banner_form.save(commit=False)
            banner.group = banner_form.cleaned_data['group']
            banner.status = banner_form.cleaned_data['status']
            banner.save()

            # Generate entry objects for each form in the entry formset
            for form in formset:
                e = form.save(commit=False)
                e.banner = banner
                e.save()
                form.save_m2m()

                messages.add_message(request, messages.SUCCESS,
                                     "Registrert aktivitet " +
                                     e.banner.group +
                                     ": " + e.caption + " (" + str(e.group) +") - "
                )

            return redirect('core:BannerView')
        else:
            banner_form = BannerAddForm(request.POST, prefix='banner')
            formset = BannersFormSet(request.POST,request.FILES)

            for dict in formset.errors:
                messages.add_message(request, messages.ERROR, dict)

            context = {
                       'banner_form': banner_form,
                       'formset': formset,
                       }
            return render(request, 'banner/add-banners.html', context)

    else:
        banner_form = BannerAddForm(prefix='banner')
        formset = BannersFormSet(queryset=qs)
        context = {
                   'banner_form': banner_form,
                   'formset': formset,
                   }
        return render(request, 'banner/add-banners.html', context)