from rest_framework.decorators import api_view
from rest_framework.response import Response

from crm_system.company_api.models import Company
from crm_system.company_api.serializer import CompanySerializer


@api_view(["GET"])
def company_list(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def company_create(request):
    serializer = CompanySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)
