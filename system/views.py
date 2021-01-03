from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from system.forms import StoreAddForm
from system.models import Store


def setting(request):
    #return HttpResponse('1')

    setting = Store.objects.get(pk=1)
    fields = '__all__'

    context={'setting':setting,

             }
    def get_object(self, queryset=None):
        if "pk" not in self.kwargs:
            self.kwargs['pk'] = None
        obj, created = Store.objects.get_or_create(pk=self.kwargs.get('id' ,None),
                                                   )

        return obj
    return render(request,'setting.html',context)


def update_setting(request):
    store = Store.objects.get(id=request.user.id)
    forms = StoreAddForm(instance=store)
    if request.method == 'POST':
        forms = StoreAddForm(request.POST, request.FILES, instance=store)
        if forms.is_valid():
            forms.save()
    context = {
        'store':store,
        'forms': forms
    }
    return render(request, 'setting.html', context)

