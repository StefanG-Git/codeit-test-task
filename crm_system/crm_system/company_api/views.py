from django.http.response import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from crm_system.company_api.models import Company
from crm_system.company_api.serializer import CompanySerializer


class CompanyListAPIView(APIView):
    def get(self, request):
        data = Company.objects.all()
        serializer = CompanySerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailAPIView(APIView):
    def get_company_by_pk(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        company = self.get_company_by_pk(pk)
        serializer = CompanySerializer(company)

        return Response(serializer.data)

    def put(self, request, pk):
        company_to_update = self.get_company_by_pk(pk)
        serializer = CompanySerializer(company_to_update, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company_to_delete = self.get_company_by_pk(pk)
        company_to_delete.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
