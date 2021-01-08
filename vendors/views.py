
from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404
from catalog.models.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from accounts.models import  User

from vendors.forms import StoreEditForm, StoreAddForm
from vendors.models import Store


@login_required  # Check login
def store_list(request):
    stores = Store.objects.all()
    current_user = request.user  # Access User Session information
    # setting = Store.objects.get(pk=1)
    # profile = User.objects.get(user.id)
    context = {'stores': stores,

               }
    return render(request, 'stores-list.html', context)


def store_page(request, id):
    store = Store.objects.get(id=id)

    context = {'store': store,
               }
    return render(request, 'store_page.html', context)


def create_success(request, id):
    user = User.objects.filter(user_id=id)

    context = {'user': user,
               }
    return render(request, 'store-page/create-success.html', context)


class AddStore(CreateView):
    model = Store
    template_name = 'store-page/become-vendor.html'
    form_class = StoreAddForm

    def get_initial(self):
        self.initial.update({'vendor': self.request.user})
        return self.initial

    success_url = reverse_lazy('vendors:create_success')


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
