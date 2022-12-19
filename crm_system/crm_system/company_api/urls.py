from django.urls import path

from crm_system.company_api.views import CompanyListAPIView, CompanyDetailAPIView

urlpatterns = [
    path('', CompanyListAPIView.as_view(), name='company list'),
    path('<int:pk>/', CompanyDetailAPIView.as_view(), name='company details'),
]
