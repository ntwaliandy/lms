from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('apply', views.user_apply, name='user_apply'),
    path('permit-apply', views.permit_apply, name='permit-apply'),
    path('group-apply', views.group_apply, name='group-apply'),
    path('my-loans', views.my_loans, name='my-loans'),
    path('my-payments', views.my_payments, name='my-payments'),
    path('support', views.support, name='support'),
    path('about', views.about, name='about')
]