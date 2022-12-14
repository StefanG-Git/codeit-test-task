from django.urls import path

from crm_system.company_api.views import company_list

urlpatterns = [
    path('list/', company_list, name='companies list'),
]