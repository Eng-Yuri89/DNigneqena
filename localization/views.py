from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.conf import settings
from django.utils import translation
# Create your views here.
from django.views.generic import CreateView, UpdateView, DeleteView

from DNigne import settings
from accounts.models import User
from localization.models import Home, Language


def index(request):
    context = dict()

    context['a'] = Home.objects.all()[2]
    context['b']= _("How are you?")


    return render(request, 'front/index.html', context)

def all_lang(request):
    lang = Language.objects.filter(status='True')

    context = {
        'lang': lang,

    }
    return render(request, 'lang-admin.html', context)

class AddLang(CreateView):
    model = Language
    template_name = 'add-lang.html'
    fields = '__all__'

    success_url = reverse_lazy('localization:all_lang')

class EditLang(UpdateView):
    model = Language
    fields = '__all__'
    template_name = 'edit-setting.html'
    success_url = reverse_lazy('localization:all_lang')


class DeleteLang(DeleteView):
    model = Language
    template_name = 'message/confirm_delete.html'
    success_url = reverse_lazy('localization:all_lang')

    def get_object(self, *args, **kwargs):
        obj = super(DeleteLang, self).get_object(*args, **kwargs)

        return obj




def change_language(request):
    response = HttpResponseRedirect('/')
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            if language != settings.LANGUAGE_CODE and [lang for lang in settings.LANGUAGES if lang[0] == language]:
                redirect_path = f'/{language}/'
            elif language == settings.LANGUAGE_CODE:
                redirect_path = '/'
            else:
                return response
            from django.utils import translation
            translation.activate(language)
            response = HttpResponseRedirect(redirect_path)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response


def selectlanguage(request):
    if request.method == 'POST':  # check post
        cur_language = translation.get_language()
        lasturl= request.META.get('HTTP_REFERER')
        lang = request.POST['language']
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY]=lang
        #return HttpResponse(lang)
        return HttpResponseRedirect("/"+lang)



#@login_required(login_url='/login') # Check login
def savelangcur(request):
    lasturl = request.META.get('HTTP_REFERER')
    curren_user = request.user
    language=Language.objects.get(code=request.LANGUAGE_CODE[0:2])
    #Save to User profile database
    data = User.objects.get(user_id=curren_user.id )
    data.language_id = language.id
    data.currency_id = request.session['currency']
    data.save()  # save data
    return HttpResponseRedirect(lasturl)