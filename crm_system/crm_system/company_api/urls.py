from django.urls import path

from crm_system.company_api.views import CompanyList, CompanyCreate, CompanyView

urlpatterns = [
    path('list/', CompanyList.as_view(), name='company list'),
    path('create/', CompanyCreate.as_view(), name='company create'),
    path('<int:pk>/', CompanyView.as_view(), name='company action'),
]