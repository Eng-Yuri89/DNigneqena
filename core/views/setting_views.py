from django.contrib import messages
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from core.forms.seeting_forms import SettingAddForm, SettingLangAddForm
from core.models.models import Setting, SettingLang, langlist
from localization.models import Language


def setting(request):
    setting = Setting.objects.first()
    setting_lang = SettingLang.objects.first()
    context = {'setting': setting,
               'setting_lang':setting_lang,

               }
    def get_object(self, queryset=None):
        if "pk" not in self.kwargs:
            self.kwargs['pk'] = None
        obj, created = Setting.objects.get_or_create(pk=self.kwargs.get('id', None),
                                                     )

        return obj

    return render(request, 'setting.html', context)

def add_setting(request):

    langlist = Language.objects.filter(status=True)
    if request.method == "POST":
        #langlist=Language.objects.filter(status=True)
        form = SettingAddForm(request.POST or None, request.FILES or None)
        lang_form = SettingLangAddForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('images')
        if form.is_valid() and lang_form.is_valid():
            print(request.POST)
            setting_created = True
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            image = files.cleaned_data['image']
            facebook = form.cleaned_data['facebook']
            instagram = form.cleaned_data['instagram']
            twitter = form.cleaned_data['twitter']
            youtube = form.cleaned_data['youtube']
            status = form.cleaned_data['status']
            setting_id = form.cleaned_data['setting_id']
            if not setting_id:
                print(request.POST)
                setting_obj = Setting.objects.create(email=email,phone=phone,
                                                     image=image,facebook=facebook,instagram=instagram,
                                                     twitter=twitter,youtube=youtube,status=status,
                                                     )  # create will create as well as save too in db.
                for k in langlist():
                    lang_obj, created = SettingLang.objects.get_or_create(name=k)
                    lang_obj.title = k.title

                    setting_obj.SettingLang.add(lang_obj)  # it won't add duplicated as stated in django docs
            else:
                # handling all cases of the tags
                print(request.POST)
                setting_obj = Setting.objects.get(id=setting_id)

                setting_created = False

            setting_obj.email = email
            setting_obj.phone = phone
            setting_obj.image = image
            setting_obj.facebook=facebook
            setting_obj.instagram=instagram
            setting_obj.twitter=twitter
            setting_obj.youtube=youtube
            setting_obj.status=status

            print(request.POST)
            setting_obj.save()  # last_modified field won't update on chaning other model field, save() trigger change
            # return reverse('core:catalog')
            return HttpResponseRedirect('/admin/setting', setting_created)
            # return render(request,template_name='admin/pages/products-admin.html')
            # return getNoteResponseData(product_obj, tags, product_created)
        else:
            print("Form invalid, see below error msg")
            print(request.POST)
            print(form.errors)
            messages.error(request, "Error")
    # if GET method form, or anything wrong then we will create blank form
    else:

        form = SettingAddForm()
        lang_form=SettingLangAddForm()

    # return HttpResponseRedirect('/')
    return render(request, 'add-setting.html', {'form': form,'lang_form':lang_form,'langlist':langlist})



def update_setting(request):
    lang =Language.objects.all()
    try:
        setting = Setting.objects.first()
        lang_setting = SettingLang.objects.first()
        forms = SettingAddForm(instance=setting)
        lang_form = SettingLangAddForm
        if request.method == 'POST':
            forms = SettingAddForm(request.POST, request.FILES, instance=setting)
            lang_form = SettingLangAddForm(request.POST)
            if forms.is_valid() and  lang_form.is_valid():
                lang_form.save(commit=False)
                forms.save(commit=False)

        context = {
            'lang':lang,
            'setting': setting,
            'lang_setting':lang_setting,
            'forms': forms,
            'lang_form':lang_form,
        }
        return render(request, 'setting.html', context)
    except Setting.DoesNotExist:
        setting = None

    forms = SettingAddForm(instance=setting)
    lang_form = SettingLangAddForm
    if request.method == 'POST':
        forms = SettingAddForm(request.POST, request.FILES, instance=setting)
        lang_form = SettingLangAddForm(request.POST)
        if forms.is_valid() and lang_form.is_valid():
            lang_form.save(commit=False)
            forms.save(commit=False)

    context = {
        'lang': lang,
        'setting': setting,
        'forms': forms,
        'lang_form': lang_form,
    }

    return render(request, 'setting.html',context)


