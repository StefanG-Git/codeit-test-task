from django.http.response import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from crm_system.company_api.models import Company
from crm_system.company_api.serializer import CompanySerializer


class CompanyListAPIView(APIView):
    def get(self, request):
        # Get all companies from the db
        data = Company.objects.all()
        # Serialize the data of all companies if any
        serializer = CompanySerializer(data, many=True)
        # Return all companies as list of jsons if any else empty list and corresponding status code
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Serialize the provided data
        serializer = CompanySerializer(data=request.data)
        # Check if all data is valid
        if serializer.is_valid():
            # Create new company and save it in the db
            serializer.save()
            # Return the new company as json and corresponding status code
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return the corresponding error message and status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailAPIView(APIView):
    def get_company_by_pk(self, pk):
        try:
            # Return company with the provided pk if exists
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            # Return the corresponding error message and status code
            raise Http404

    def get(self, request, pk):
        # Get company with the provided pk if exists
        company = self.get_company_by_pk(pk)
        # Serialize the data of the company
        serializer = CompanySerializer(company)
        # Return the company as json and corresponding status code
        return Response(serializer.data)

    def put(self, request, pk):
        # Get company with the provided pk if exists
        company_to_update = self.get_company_by_pk(pk)
        # Serialize the provided data
        serializer = CompanySerializer(company_to_update, data=request.data, partial=True)
        # Check if data is valid
        if serializer.is_valid():
            # Update the data of the company in the db
            serializer.save()
            # Return the updated company as json and corresponding status code
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Return the corresponding error message and status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Get company with the provided pk if exists
        company_to_delete = self.get_company_by_pk(pk)
        # Delete the company from the db
        company_to_delete.delete()
        # Return the corresponding status code
        return Response(status=status.HTTP_204_NO_CONTENT)
