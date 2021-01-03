from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from SiteSetting.models import Store
from accounts.admin import UserAdmin
from accounts.forms import GuestForm, UserAdminChangeForm
from django.utils.http import is_safe_url
from accounts.signals import user_logged_in
from django.views.generic import CreateView, TemplateView, UpdateView
from django.views import View

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from accounts.models import GuestEmail, User
from accounts.forms import UserLoginForm, UserRegisterForm



@login_required # Check login
def profile(request):
    #category = Category.objects.all()
    current_user = request.user  # Access User Session information
    setting = Store.objects.get(pk=1)
    #profile = User.objects.get(user.id)
    context = {'current_user': current_user,
               'profile':profile,
               'setting':setting}
    return render(request, 'accounts/profile.html', context)


def update_profile(request):
    user = User.objects.get(id=request.user.id)
    forms = UserAdminChangeForm(instance=user)
    if request.method == 'POST':
        forms = UserAdminChangeForm(request.POST, request.FILES, instance=user)
        if forms.is_valid():
            forms.save()
    context = {
        'user':user,
        'forms': forms
    }
    return render(request, 'accounts/test.html', context)

class AddProfile(CreateView):
    model = User
    template_name = 'accounts/UpdateProfile.html'
    fields = '__all__'
    # uccess_url =redirect('home:product_admin')
    success_url = reverse_lazy('accounts:user_profile')


class EditProfile(UpdateView):
    model = User
    fields = '__all__'
    template_name = 'admin/pages/edit-category.html'
    success_url = reverse_lazy('accounts:user_profile')


class UserLoginView(View):
    """
    Description:Will be used to login and logout users.\n
    """
    template_name = 'admin/login.html'

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
                    return redirect("/admin/")

            else:
                print("error")
                return redirect("/admin/login/")

        context = {
            "title": "Login",
            "form": form
        }
        return render(request, self.template_name, context)



def logout_func(request):
    logout(request)

    return render(request, 'admin/login.html')
# class RegisterView(CreateView):
#     form_class = UserRegisterForm
#     template_name = 'accounts/register.html'
#     success_url = '/login/'


class RegisterView(View):
    """
    Description:View to create a new user.\n
    """
    template_name = 'accounts/create-user.html'

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        context = {
            "title": "Register",
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST or None)
        next_ = request.GET.get('next')

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            login(request, user)
            if next_:
                return redirect(next_)
            return redirect("/")

        context = {
            "title": "Register",
            "form": form
        }
        return render(request, self.template_name, context)


def guest_user_view(request):
    '''
    handle guest user creation\n
    '''
    form = GuestForm(request.POST or None)

    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)

        else:
            return redirect("/accounts/register/")

    return redirect("/accounts/register/")
