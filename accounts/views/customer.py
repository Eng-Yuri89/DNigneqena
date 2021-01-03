from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.http import is_safe_url
from django.views import View
from django.views.generic import CreateView

from accounts.forms import UserRegisterForm, UserLoginForm, CustomerRegisterForm
from accounts.models import User

from accounts.signals import user_logged_in


@login_required(login_url='/login') # Check login
def profile(request):
    #category = Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = User.objects.get(user_id=current_user.id)
    context = {'current_user': current_user,
               'profile':profile}
    return render(request,'front/UsersAccount/CustomerProfile.html',context)

class CustomerLoginView(View):
    """
    Description:Will be used to login and logout users.\n
    """
    template_name = 'front/UsersAccount/UserLogin.html'

    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        context = {
            "title": "Login",
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST or None)

        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                user_logged_in.send(
                    user.__class__,
                    instance=user,
                    request=request
                )
                try:
                    del request.session['guest_email_id']

                except:
                    pass

                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)

                else:
                    return redirect("/home/")

            else:
                print("error")
                return redirect("/home/login/")

        context = {
            "title": "Login",
            "form": form
        }
        return render(request, self.template_name, context)







class CustomerRegister(CreateView):
    model = User
    form_class = CustomerRegisterForm
    template_name = 'front/UsersAccount/CustomerRegister.html'

    # uccess_url =redirect('home:product_admin')
    success_url = reverse_lazy('home:index')

def customer_logout(request):
    logout(request)

    return HttpResponseRedirect('/')
