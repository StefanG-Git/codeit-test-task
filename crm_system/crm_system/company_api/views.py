from django.shortcuts import render
from django.http import JsonResponse
from crm_system.company_api.models import Company


def companies_list(request):
    companies = Company.objects.all()
    companies_python = list(companies.values())
    return JsonResponse({
        'companies': companies_python
    })
