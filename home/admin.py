from django.contrib import admin
from .models import Apply, GroupApply, Support, PermitApply
# Register your models here.
admin.site.register(Apply)
admin.site.register(GroupApply)
admin.site.register(Support)
admin.site.register(PermitApply)