from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from DNigne.mixins import LoginRequiredMixin

from catalog.models.models import Product



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


from accounts.admin import UserAdmin
from accounts.forms import GuestForm, UserAdminChangeForm
from django.utils.http import is_safe_url
from accounts.signals import user_logged_in
from django.views.generic import CreateView, TemplateView, UpdateView
from django.views import View, generic

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from accounts.models import GuestEmail, User
from accounts.forms import UserLoginForm, UserRegisterForm
from vendors.forms import StoreEditForm
from vendors.models import Store


@login_required  # Check login
def store_list(request):
    stores = Store.objects.all()
    current_user = request.user  # Access User Session information
    #setting = Store.objects.get(pk=1)
    # profile = User.objects.get(user.id)
    context = {'stores': stores,

               }
    return render(request, 'stores-list.html', context)



def store_page(request, id):
    store = Store.objects.get(id=id)

    context = {'store': store,
              }
    return render(request, 'store_page.html', context)

class AddStore(CreateView):
    model = Store
    template_name = 'create_store.html'
    fields = '__all__'
    # uccess_url =redirect('home:product_admin')
    success_url = reverse_lazy('waiting_for_activation.html')



def edit_store(request):
    store = Store.objects.get(id=request.store.id)
    forms = StoreEditForm(instance=store)
    if request.method == 'POST':
        forms = StoreEditForm(request.POST, request.FILES, instance=store)
        if forms.is_valid():
            forms.save()
    context = {
        'user': store,
        'forms': forms
    }
    return render(request, 'store_page.html', context)



def store_delete(request, user_id):
    store = Store.objects.get(id=user_id)
    store.is_delete = True
    store.save()
    return redirect('vendors')




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
#     template_name = 'accounts/create_store.html'
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
















# Seller product list and details

class SellerProductDetailRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Product, pk=kwargs['pk'])
        return obj.get_absolute_url()











# Seller transaction lists
'''''
class SellerTransactionListView(SellerAccountMixin, ListView):
	model = Transaction
	template_name = "sellers/transaction_list_view.html"

	def get_queryset(self):
		return self.get_transactions()



# Seller dashboard

class SellerDashboard(SellerAccountMixin, FormMixin, View):
    form_class = NewSellerForm
    success_url = "/seller/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        apply_form = self.get_form()  # NewSellerForm()
        account = self.get_account()
        exists = account
        active = None
        context = {}
        if exists:
            active = account.active
        if not exists and not active:
            context["title"] = "Apply for Account"
            context["apply_form"] = apply_form
        elif exists and not active:
            context["title"] = "Account Pending"
        elif exists and active:
            context["title"] = "Seller Dashboard"
            context["products"] = self.get_products()
            transactions_today = self.get_transactions_today()
            context["transactions_today"] = transactions_today
            context["today_sales"] = self.get_today_sales()
            context["total_sales"] = self.get_total_sales()
            context["transactions"] = self.get_transactions().exclude(pk__in=transactions_today)[:5]
        else:
            pass

        return render(request, "sellers/dashboard.html", context)

    def form_valid(self, form):
        valid_data = super(SellerDashboard, self).form_valid(form)
        obj = SellerAccount.objects.create(user=self.request.user)
        return valid_data
'''