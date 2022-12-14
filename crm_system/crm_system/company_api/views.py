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


@api_view(["GET", "PUT", "DELETE"])
def company(request, pk):
    current_company = Company.objects.get(pk=pk)
    if request.method == "GET":
        serializer = CompanySerializer(current_company)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = CompanySerializer(current_company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

