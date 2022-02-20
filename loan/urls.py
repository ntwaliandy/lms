from django.urls import path, re_path
from . import views

app_name = 'loan'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('manage-loans/', views.manage_loans, name='manage-loans'),
    path('manage-group-loans/', views.manage_group_loans, name='manage_group_loans'),
    path('loan-approve/', views.loan_approve, name='loan-approve' ),
    path('group-loan-approve/', views.group_loan_approve, name='group-loan-approve'),
    path('group-loan-remove/', views.group_loan_remove, name='group-loan-remove'),
    path('loan-remove/', views.loan_remove, name='loan-remove'),
    path('loan-complete/', views.loan_complete, name='loan-complete'),
    path('group-loan-complete', views.group_loan_complete, name='group-loan-complete'),
    path('add-payment', views.add_payment, name='add-payment'),
    path('group-add-payment', views.group_add_payment, name='group-add-payment'),
    path('payment-record', views.payment_record, name='payment-record'),
    path('group-payment-record', views.group_payment_record, name='group-payment-record'),
    re_path(r'^(?P<loan_id>[0-9]+)/$', views.loan_details, name='loan-details'),
    path('all-clients', views.all_clients, name='all-clients'),
    path('staff', views.staff, name='staff'),
    path('complaints', views.complaints, name='complaints'),
    re_path(r'^view_reply/(?P<error_id>[0-9]+)/$', views.reply, name='reply'),
    re_path(r'^done/(?P<quest_id>[0-9]+)/$', views.done, name='done'),
    re_path(r'^group/(?P<group_l_id>[0-9]+)/$', views.group_details, name='group-details'),
    path('send-report', views.send_report, name='send-report')

]