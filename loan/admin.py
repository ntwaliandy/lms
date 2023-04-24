from django.contrib import admin
from .models import AddPayment, GroupAddPayment, Replies, AddPermitPayment, FileUpload, BodaApply, BodaWeeklyPay


class permitAddPaymentAdmin(admin.ModelAdmin):
    list_display = ("permit_id", "payment_fee", "phone_number", "status", "reference", "date", "transaction_id")
    search_fields = ["permit_id", "payment_fee", "phone_number", "status", "reference", "date", "transaction_id"]

class BodaBodaAdmin(admin.ModelAdmin):
    list_display = ("boda_guy_firstName", "boda_guy_lastName", "boda_numberPlate", "weekly_pay", "deposits", "balance", "final_amount")
    search_fields = ["boda_guy_firstName", "boda_guy_lastName", "boda_numberPlate", "weekly_pay", "deposits", "balance", "final_amount"]

class BodaWeeklyAdmin(admin.ModelAdmin):
    list_display = ("boda_id", "boda_firstName", "boda_lastName", "payment_fee", "date")
    search_fields = ["boda_id", "boda_firstName", "boda_lastName", "payment_fee", "date"]

# Register your models here.
admin.site.register(AddPayment)
admin.site.register(GroupAddPayment)
admin.site.register(Replies)
admin.site.register(AddPermitPayment, permitAddPaymentAdmin)
admin.site.register(FileUpload)
admin.site.register(BodaApply, BodaBodaAdmin)
admin.site.register(BodaWeeklyPay, BodaWeeklyAdmin)
