from django.urls import path

from crm_system.employee_api.views import EmployeeListAPIView, EmployeeDetailAPIView

urlpatterns = [
    path('', EmployeeListAPIView.as_view(), name='employee list'),
    path('<int:pk>/', EmployeeDetailAPIView.as_view(), name='employee action'),
]
