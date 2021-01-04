from django.conf import settings
from django.db import models

from accounts.models import User
from catalog.models.seller_models import SellerProduct


class Transaction(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    product = models.ForeignKey(SellerProduct , on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99, null=True,)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    success = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" %(self.id)
