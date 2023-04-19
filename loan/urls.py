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
    re_path(r'^pay-details/(?P<ref>(.*))/$', views.pay_details, name='pay-details'),
    re_path(r'^fee-details/(?P<loan_id>(.*))/$', views.fee_details, name='fee-details'),
    path('group-loan-complete', views.group_loan_complete, name='group-loan-complete'),
    path('add-payment', views.add_payment, name='add-payment'),
    path('manual-add-payment', views.manual_add_payment, name='manual-add-payment'),
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
    path('send-report', views.send_report, name='send-report'),

    # permit section

    path('permit-dashboard', views.permit_dashboard, name='permit-dashboard'),
    path('permit-add-payment', views.permit_add_payment, name='permit-add-payment'),
    path('permit-payment-details', views.permit_payment_details, name='permit-payment-details'),
    re_path(r'^permit-pay-details/(?P<ref>(.*))/$', views.permit_pay_details, name='permit-pay-details'),
    path('permit-clients', views.permit_clients, name='permit-clients'),
    path('files-upload', views.files_upload, name='files-upload'),
    path('search-client', views.search_client, name='search-client'),
    path('search-client-trigger', views.search_client_trigger, name='search-client-trigger'),
    re_path(r'^file-details/(?P<permitId>[0-9]+)/$', views.file_details, name='file-details'),
    path('permit-logs', views.permit_logs, name='permit-logs'),
    path('loan-logs', views.loan_logs, name='loan-logs'),
    re_path(r'^edit_permit/(?P<permitID>[0-9]+)/$', views.permit_edit_details, name='edit-permit'),
    path('client-csv', views.client_csv, name='client-csv'),
    path('post-permit-edit', views.post_permit_edit, name='post-permit-edit'),

    # boda bodas
    path('add-boda', views.add_boda, name="add-boda"),
    path('boda-dashboard', views.boda_dashboard, name="boda-dashboard"),
    path('search-client-boda', views.search_client_boda, name='search-client-boda'),
    path('manual-add-boda-payment', views.manual_add_boda_pay, name="add-boda-pay"),
    path('search-boda', views.search_boda_trigger, name="search-boda"),
    path('weekly-logs', views.weekly_logs, name="weekly-logs"),
    path('full-boda-logs', views.full_week_logs, name="full-week-logs"),
    re_path(r'^boda-details/(?P<bodaId>[0-9]+)/$', views.boda_details, name='boda-detail'),
]