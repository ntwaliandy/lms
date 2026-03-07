from django.contrib import admin
from .models import AddPayment, BodaInformation, BodaInventory, CashFlow, GroupAddPayment, ImpoundedBike, Replies, AddPermitPayment, FileUpload, BodaApply, BodaWeeklyPay


class permitAddPaymentAdmin(admin.ModelAdmin):
    list_display = ("permit_id", "payment_fee", "phone_number", "status", "reference", "date", "transaction_id")
    search_fields = ["permit_id", "payment_fee", "phone_number", "status", "reference", "date", "transaction_id"]

class BodaBodaAdmin(admin.ModelAdmin):
    list_display = ("boda_guy_firstName", "boda_guy_lastName", "boda_numberPlate", "status", "weekly_pay", "deposits", "balance", "final_amount")
    search_fields = ["boda_guy_firstName", "boda_guy_lastName", "boda_numberPlate", "status", "weekly_pay", "deposits", "balance", "final_amount"]

class BodaWeeklyAdmin(admin.ModelAdmin):
    list_display = ("boda_id", "boda_firstName", "boda_lastName", "payment_fee", "date")
    search_fields = ["boda_id", "boda_firstName", "boda_lastName", "payment_fee", "date"]

class CashFlowAdmin(admin.ModelAdmin):
    list_display = ("cash_id", "expenditures", "collections", "banked_balance", "date")
    search_fields = ["cash_id", "expenditures", "collections", "banked_balance", "date"]

class BodaInfoAdmin(admin.ModelAdmin):
    list_display = ("numberPlate", "rider", "amountBought", "whereBought", "LogBookNames", "demandedAmount", "isCompleted")
    search_fields = ["numberPlate", "rider", "amountBought", "whereBought", "LogBookNames", "demandedAmount", "isCompleted"]

class BodaInventoryAdmin(admin.ModelAdmin):
    list_display = ("number_plate", "boda_type", "colour", "chassis_no", "engine_no", "amount_bought_at", "date_purchased", "status", "buyer_name", "amount_sold_for", "date_sold", "boda_apply_id")
    list_filter = ("status",)
    search_fields = ["number_plate", "boda_type", "chassis_no", "engine_no", "buyer_name", "buyer_phone", "buyer_id", "boda_apply_id"]
    readonly_fields = ("created_at",)

class ImpoundedBikeAdmin(admin.ModelAdmin):
    list_display = ("number_plate", "client_name", "client_phone", "date_impounded", "deficit_at_impound", "amount_demanded", "status", "date_returned", "days_held")
    list_filter = ("status",)
    search_fields = ["number_plate", "client_name", "client_phone", "boda_id"]
    readonly_fields = ("created_at",)

# Register your models here.
admin.site.register(AddPayment)
admin.site.register(GroupAddPayment)
admin.site.register(Replies)
admin.site.register(AddPermitPayment, permitAddPaymentAdmin)
admin.site.register(FileUpload)
admin.site.register(BodaApply, BodaBodaAdmin)
admin.site.register(BodaWeeklyPay, BodaWeeklyAdmin)
admin.site.register(CashFlow, CashFlowAdmin)
admin.site.register(BodaInformation, BodaInfoAdmin)
admin.site.register(BodaInventory, BodaInventoryAdmin)
admin.site.register(ImpoundedBike, ImpoundedBikeAdmin)
