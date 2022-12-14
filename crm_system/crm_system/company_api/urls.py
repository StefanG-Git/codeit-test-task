from django.urls import path

from crm_system.company_api.views import company_list, company_create

urlpatterns = [
    path('list/', company_list, name='company list'),
    path('create/', company_create, name='company create'),
]