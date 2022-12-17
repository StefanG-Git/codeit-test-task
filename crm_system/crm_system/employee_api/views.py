from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from crm_system.employee_api.models import Employee
from crm_system.employee_api.serializer import EmployeeSerializer


class EmployeeListAPIView(APIView):
    def get(self, request):
        data = Employee.objects.all()
        serializer = EmployeeSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailAPIView(APIView):
    def get_employee_by_pk(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        employee = self.get_employee_by_pk(pk)
        serializer = EmployeeSerializer(employee)

        return Response(serializer.data)

    def put(self, request, pk):
        employee_to_update = self.get_employee_by_pk(pk)
        serializer = EmployeeSerializer(employee_to_update, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee_to_delete = self.get_employee_by_pk(pk)
        employee_to_delete.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
