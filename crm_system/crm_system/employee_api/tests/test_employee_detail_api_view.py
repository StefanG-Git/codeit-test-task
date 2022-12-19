from django.urls import reverse
from rest_framework import status

from crm_system.employee_api.tests.common_employee_test_config import EmployeeAPIViewTestCase


class TestEmployeeDetailAPIView(EmployeeAPIViewTestCase):
    EMPLOYEE_DETAIL_URL_NAME = 'employee details'

    def test_get__when_pk_does_not_exists__expect_not_found(self):
        expected_info_message = 'Not found.'

        response = self.client.get(reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': 1}))

        self.assertEqual(expected_info_message, response.json()['detail'])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get__when_pk_exists__expect_to_get_employee_with_pk(self):
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.get(reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}))

        self.assertEqual(self.VALID_FIRST_NAME, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(self.VALID_LAST_NAME, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(self.VALID_DATE_OF_BIRTH, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual('/' + self.TEST_PHOTO_TO_DELETE_PATH, response.json()[self.PHOTO_FIELD])
        self.assertEqual(self.VALID_POSITION, response.json()[self.POSITION_FIELD])
        self.assertEqual(str(self.VALID_SALARY), response.json()[self.SALARY_FIELD])
        self.assertEqual(self.company.id, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
