from django.contrib import admin
from .models import Apply, GroupApply, Support, PermitApply, SmsCallBack
from django.contrib import admin


class permitAdmin(admin.ModelAdmin):
    list_display = ("permit_id", "first_name", "last_name", "service", "deposits", "balance", "final_amount")
    search_fields = ["permit_id", "first_name", "last_name", "service", "deposits", "balance", "final_amount"]

class smsAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone_number", "amount", "network", "status", "date")
    search_fields = ["first_name", "last_name", "phone_number", "amount", "network", "status", "date"]

# Register your models here.
admin.site.register(Apply)
admin.site.register(GroupApply)
admin.site.register(Support)
admin.site.register(PermitApply, permitAdmin)
admin.site.register(SmsCallBack, smsAdmin)