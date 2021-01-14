from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from core.forms.seeting_forms import SettingAddForm
from core.models import Setting


def setting(request):
    setting = Setting.objects.first()
    context = {'setting': setting,

               }
    def get_object(self, queryset=None):
        if "pk" not in self.kwargs:
            self.kwargs['pk'] = None
        obj, created = Setting.objects.get_or_create(pk=self.kwargs.get('id', None),
                                                     )

        return obj

    return render(request, 'setting.html', context)


def update_setting(request):
    try:
        setting = Setting.objects.first()
        forms = SettingAddForm(instance=setting)
        if request.method == 'POST':
            forms = SettingAddForm(request.POST, request.FILES, instance=setting)
            if forms.is_valid():
                forms.save()
        context = {
            'setting': setting,
            'forms': forms
        }
        return render(request, 'setting.html', context)
    except Setting.DoesNotExist:
        setting = None

    forms = SettingAddForm()
    if request.method == 'POST':
        forms = SettingAddForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
    context = {

        'forms': forms
    }

    return render(request, 'setting.html',context)


