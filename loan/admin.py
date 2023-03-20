from django.contrib import admin
from .models import AddPayment, GroupAddPayment, Replies, AddPermitPayment, FileUpload


class permitAddPaymentAdmin(admin.ModelAdmin):
    list_display = ("permit_id", "payment_fee", "phone_number", "status", "reference", "date", "transaction_id")
    search_fields = ["permit_id", "payment_fee", "phone_number", "status", "reference", "date", "transaction_id"]



# Register your models here.
admin.site.register(AddPayment)
admin.site.register(GroupAddPayment)
admin.site.register(Replies)
admin.site.register(AddPermitPayment, permitAddPaymentAdmin)
admin.site.register(FileUpload)
