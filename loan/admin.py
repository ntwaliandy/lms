from django.contrib import admin
from .models import AddPayment, GroupAddPayment, Replies, AddPermitPayment
# Register your models here.
admin.site.register(AddPayment)
admin.site.register(GroupAddPayment)
admin.site.register(Replies)
admin.site.register(AddPermitPayment)
