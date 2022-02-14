from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('user-login', views.user_login, name='user_login'),
    path('user-reg', views.user_reg, name='user_reg'),
    path('logout-user', views.logout_user, name="logout_user"),
    path('admin-login', views.admin_login, name='admin-login'),
    path('logout-admin', views.admin_logout, name='admin-logout')
]