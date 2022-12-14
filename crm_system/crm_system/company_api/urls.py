from django.urls import path

from crm_system.company_api.views import companies_list

urlpatterns = [
    path('list/', companies_list, name='companies list'),
]