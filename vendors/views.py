from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic.base import RedirectView

from accounts.models import User
from catalog.models.models import Product
from vendors.forms import StoreEditForm, StoreAddForm
from vendors.models import Store


@login_required  # Check login
def store_list(request):
    store = Store.objects.all()
    current_user = request.user  # Access User Session information
    # setting = Store.objects.get(pk=1)
    # profile = User.objects.get(user.id)
    context = {'store': store,

               }
    return render(request, 'stores-list.html', context)


def admin_dashboard(request, id):
    current_user = request.user  # Access User Session information
    store = Store.objects.get(id=id)

    context = {'store': store,
               }
    return render(request, 'store_page.html', context)

@login_required(login_url='/home/login/') # Check login
def vendor_dashboard(request ,vendor=None):
    vendor = request.user  # Access User Session information
    store = Store.objects.get(vendor=vendor)


    context = {'store': store,


               }
    return render(request, 'vendor-dashboard.html', context)


def create_success(request, id):
    user = User.objects.filter(user_id=id)

    context = {'user': user,
               }
    return render(request, 'store-page/create-success.html', context)

def become_seller(request, id):
    forms = StoreAddForm
    if request.method == 'POST':

        print(request.POST)
        forms = StoreAddForm(request.POST, request.FILES)
        if forms.is_valid():
            store = forms.save(commit=False)
            store.vendor = request.user
            store.save()
            # Add this to check if the email already exists in your database or not
            # store.save()
            return render(request, 'store-page/create-success.html', )
    else:
        forms = StoreAddForm(request.POST, request.FILES)
        return render(request, 'store-page/become-seller.html', {'forms': forms})
    return render(request, 'store-page/become-seller.html', {'forms': forms})

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


# Seller catalog list and details

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
