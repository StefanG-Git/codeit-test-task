from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from crm_system.employee_api.models import Employee
from crm_system.employee_api.serializer import EmployeeSerializer


class EmployeeListAPIView(APIView):
    def get(self, request):
        # Get all employees from the db
        data = Employee.objects.all()
        # Serialize the data of all employees if any
        serializer = EmployeeSerializer(data, many=True)
        # Return all companies as list of jsons if any else empty list and corresponding status code
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Serialize the provided data
        serializer = EmployeeSerializer(data=request.data)
        # Check if all data is valid
        if serializer.is_valid():
            # Create new employee and save it in the db
            serializer.save()
            # Return the new employee as json and status code
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Return the corresponding error message and status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailAPIView(APIView):
    def get_employee_by_pk(self, pk):
        try:
            # Return employee with the provided pk if exists
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            # Return the corresponding error message and status code
            raise Http404

    def get(self, request, pk):
        # Get employee with the provided pk if exists
        employee = self.get_employee_by_pk(pk)
        # Serialize the data of the employee
        serializer = EmployeeSerializer(employee)
        # Return the employee as json and corresponding status code
        return Response(serializer.data)

    def put(self, request, pk):
        # Get employee with the provided pk if exists
        employee_to_update = self.get_employee_by_pk(pk)
        # Serialize the provided data
        serializer = EmployeeSerializer(employee_to_update, data=request.data, partial=True)
        # Check if data is valid
        if serializer.is_valid():
            # Update the data of the employee in the db
            serializer.save()
            # Return the updated employee as json and corresponding status code
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Return the corresponding error message and status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Get employee with the provided pk if exists
        employee_to_delete = self.get_employee_by_pk(pk)
        # Delete the employee from the db
        employee_to_delete.delete()
        # Return the corresponding status code
        return Response(status=status.HTTP_204_NO_CONTENT)
