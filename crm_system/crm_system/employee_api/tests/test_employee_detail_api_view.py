from django.urls import reverse
from rest_framework import status

from crm_system.common.utils import create_image, delete_file
from crm_system.employee_api.tests.common_employee_test_config import EmployeeAPIViewTestCase


class TestEmployeeDetailAPIView(EmployeeAPIViewTestCase):
    EMPLOYEE_DETAIL_URL_NAME = 'employee details'

    UPDATED_FIRST_NAME = 'Update'
    UPDATED_LAST_NAME = 'Updated'
    UPDATED_DATE_OF_BIRTH = '2003-12-01'
    UPDATED_PHOTO_PATH = 'media/for_testing/updated_valid_size_photo.png'
    UPDATED_POSITION = 'Updater'
    UPDATED_SALARY = format(3000.25, '.2f')

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

    def test_put__when_pk_does_not_exists__expect_not_found(self):
        expected_info_message = 'Not found.'

        response = self.client.put(reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': 1}))

        self.assertEqual(expected_info_message, response.json()['detail'])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_put__when_pk_exists_and_update_all_fields_with_valid_data__expect_to_update_all_company_fields(self):
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        updated_photo = create_image(self.TEST_PHOTO_NAME, self.UPDATED_PHOTO_PATH)
        updated_test_data = {
            self.FIRST_NAME_FIELD: self.UPDATED_FIRST_NAME,
            self.LAST_NAME_FIELD: self.UPDATED_LAST_NAME,
            self.DATE_OF_BIRTH_FIELD: self.UPDATED_DATE_OF_BIRTH,
            self.PHOTO_FIELD: updated_photo,
            self.POSITION_FIELD: self.UPDATED_POSITION,
            self.SALARY_FIELD: self.UPDATED_SALARY,
            self.COMPANY_ID_FIELD: self.company.id
        }
        # Delete the initial photo because it's creating new with random name
        delete_file(self.TEST_PHOTO_TO_DELETE_PATH)

        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data=updated_test_data
        )

        self.assertEqual(self.UPDATED_FIRST_NAME, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(self.UPDATED_LAST_NAME, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(self.UPDATED_DATE_OF_BIRTH, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual('/' + self.TEST_PHOTO_TO_DELETE_PATH, response.json()[self.PHOTO_FIELD])
        self.assertEqual(self.UPDATED_POSITION, response.json()[self.POSITION_FIELD])
        self.assertEqual(str(self.UPDATED_SALARY), response.json()[self.SALARY_FIELD])
        self.assertEqual(self.company.id, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_first_name_with_valid_data__expect_to_update_first_name_only(self):
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.FIRST_NAME_FIELD: self.UPDATED_FIRST_NAME}
        )

        self.assertEqual(self.UPDATED_FIRST_NAME, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(self.VALID_LAST_NAME, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(self.VALID_DATE_OF_BIRTH, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual('/' + self.TEST_PHOTO_TO_DELETE_PATH, response.json()[self.PHOTO_FIELD])
        self.assertEqual(self.VALID_POSITION, response.json()[self.POSITION_FIELD])
        self.assertEqual(str(self.VALID_SALARY), response.json()[self.SALARY_FIELD])
        self.assertEqual(self.company.id, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_first_name_with_lower_case__expect_to_update_and_capitalize_first_name_only(self):
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.FIRST_NAME_FIELD: self.UPDATED_FIRST_NAME.lower()}
        )

        self.assertEqual(self.UPDATED_FIRST_NAME, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(self.VALID_LAST_NAME, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(self.VALID_DATE_OF_BIRTH, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual('/' + self.TEST_PHOTO_TO_DELETE_PATH, response.json()[self.PHOTO_FIELD])
        self.assertEqual(self.VALID_POSITION, response.json()[self.POSITION_FIELD])
        self.assertEqual(str(self.VALID_SALARY), response.json()[self.SALARY_FIELD])
        self.assertEqual(self.company.id, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_first_name_with_empty_str__expect_bad_request(self):
        expected_info_messages = ['This field may not be blank.']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.FIRST_NAME_FIELD: ''}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_first_name_with_1_letter_value__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has at least 2 characters.']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.FIRST_NAME_FIELD: 'J'}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_first_name_with_too_long_value__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has no more than 30 characters.']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.FIRST_NAME_FIELD: self.TOO_LONG_NAME}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_first_name_with_digits__expect_bad_request(self):
        expected_info_messages = ['First name must contains only letters']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.FIRST_NAME_FIELD: '55'}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_first_name_with_symbols__expect_bad_request(self):
        expected_info_messages = ['First name must contains only letters']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.FIRST_NAME_FIELD: '$%^^'}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_last_name_with_valid_data__expect_to_update_last_name_only(self):
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LAST_NAME_FIELD: self.UPDATED_LAST_NAME}
        )

        self.assertEqual(self.VALID_FIRST_NAME, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(self.UPDATED_LAST_NAME, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(self.VALID_DATE_OF_BIRTH, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual('/' + self.TEST_PHOTO_TO_DELETE_PATH, response.json()[self.PHOTO_FIELD])
        self.assertEqual(self.VALID_POSITION, response.json()[self.POSITION_FIELD])
        self.assertEqual(str(self.VALID_SALARY), response.json()[self.SALARY_FIELD])
        self.assertEqual(self.company.id, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_last_name_with_lower_case__expect_to_update_and_capitalize_last_name_only(self):
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LAST_NAME_FIELD: self.UPDATED_LAST_NAME.lower()}
        )

        self.assertEqual(self.VALID_FIRST_NAME, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(self.UPDATED_LAST_NAME, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(self.VALID_DATE_OF_BIRTH, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual('/' + self.TEST_PHOTO_TO_DELETE_PATH, response.json()[self.PHOTO_FIELD])
        self.assertEqual(self.VALID_POSITION, response.json()[self.POSITION_FIELD])
        self.assertEqual(str(self.VALID_SALARY), response.json()[self.SALARY_FIELD])
        self.assertEqual(self.company.id, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_last_name_with_empty_str__expect_bad_request(self):
        expected_info_messages = ['This field may not be blank.']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LAST_NAME_FIELD: ''}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_last_name_with_1_letter_value__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has at least 2 characters.']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LAST_NAME_FIELD: 'J'}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_last_name_with_too_long_value__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has no more than 30 characters.']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LAST_NAME_FIELD: self.TOO_LONG_NAME}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_last_name_with_digits__expect_bad_request(self):
        expected_info_messages = ['Last name must contains only letters']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LAST_NAME_FIELD: '55'}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_last_name_with_symbols__expect_bad_request(self):
        expected_info_messages = ['Last name must contains only letters']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LAST_NAME_FIELD: '$%^^'}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_date_of_birth_with_valid_data__expect_to_update_date_of_birth_only(self):
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DATE_OF_BIRTH_FIELD: self.UPDATED_DATE_OF_BIRTH}
        )

        self.assertEqual(self.VALID_FIRST_NAME, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(self.VALID_LAST_NAME, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(self.UPDATED_DATE_OF_BIRTH, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual('/' + self.TEST_PHOTO_TO_DELETE_PATH, response.json()[self.PHOTO_FIELD])
        self.assertEqual(self.VALID_POSITION, response.json()[self.POSITION_FIELD])
        self.assertEqual(str(self.VALID_SALARY), response.json()[self.SALARY_FIELD])
        self.assertEqual(self.company.id, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_date_of_birth_with_invalid_format_date__expect_bad_request(self):
        expected_info_messages = ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DATE_OF_BIRTH_FIELD: self.INVALID_DATE_FORMAT}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_date_of_birth_with_future_date__expect_bad_request(self):
        expected_info_messages = ['Invalid date']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DATE_OF_BIRTH_FIELD: self.FUTURE_DATE}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_date_of_birth_with_date_under_18_years__expect_bad_request(self):
        expected_info_messages = ['People under age of 18 cannot work']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DATE_OF_BIRTH_FIELD: self.UNDER_18_YEARS_DATE}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_date_of_birth_with_date_above_65_years__expect_bad_request(self):
        expected_info_messages = ['People older than 65 cannot work']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DATE_OF_BIRTH_FIELD: self.ABOVE_65_YEARS_DATE}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_photo_valid_data__expect_to_update_photo_only(self):
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        updated_image = create_image(self.TEST_PHOTO_NAME, self.UPDATED_PHOTO_PATH)
        # Delete the initial photo because it's creating new with random name
        delete_file(self.TEST_PHOTO_TO_DELETE_PATH)

        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.PHOTO_FIELD: updated_image}
        )

        self.assertEqual(self.VALID_FIRST_NAME, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(self.VALID_LAST_NAME, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(self.VALID_DATE_OF_BIRTH, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual('/' + self.TEST_PHOTO_TO_DELETE_PATH, response.json()[self.PHOTO_FIELD])
        self.assertEqual(self.VALID_POSITION, response.json()[self.POSITION_FIELD])
        self.assertEqual(str(self.VALID_SALARY), response.json()[self.SALARY_FIELD])
        self.assertEqual(self.company.id, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_photo_with_not_a_file_value__expect_bad_request(self):
        expected_info_messages = ['The submitted data was not a file. Check the encoding type on the form.']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.PHOTO_FIELD: self.TOO_LONG_NAME}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.PHOTO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_photo_with_too_big_file__expect_bad_request(self):
        expected_info_messages = ['Max file size is 1MB']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        updated_photo = create_image(self.TEST_LOGO_NAME, self.TOO_BIG_PHOTO_PATH)

        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.PHOTO_FIELD: updated_photo}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.PHOTO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_position_with_valid_data__expect_to_update_position_only(self):
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.POSITION_FIELD: self.UPDATED_POSITION}
        )

        self.assertEqual(self.VALID_FIRST_NAME, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(self.VALID_LAST_NAME, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(self.VALID_DATE_OF_BIRTH, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual('/' + self.TEST_PHOTO_TO_DELETE_PATH, response.json()[self.PHOTO_FIELD])
        self.assertEqual(self.UPDATED_POSITION, response.json()[self.POSITION_FIELD])
        self.assertEqual(str(self.VALID_SALARY), response.json()[self.SALARY_FIELD])
        self.assertEqual(self.company.id, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_position_with_empty_str__expect_bad_request(self):
        expected_info_messages = ['This field may not be blank.']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.POSITION_FIELD: ''}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.POSITION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_position_with_2_letter_value__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has at least 3 characters.']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.POSITION_FIELD: 'CE'}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.POSITION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_position_with_too_long_value__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has no more than 50 characters.']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.POSITION_FIELD: self.TOO_LONG_POSITION}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.POSITION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_salary_with_valid_data__expect_to_update_salary_only(self):
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.SALARY_FIELD: self.UPDATED_SALARY}
        )

        self.assertEqual(self.VALID_FIRST_NAME, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(self.VALID_LAST_NAME, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(self.VALID_DATE_OF_BIRTH, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual('/' + self.TEST_PHOTO_TO_DELETE_PATH, response.json()[self.PHOTO_FIELD])
        self.assertEqual(self.VALID_POSITION, response.json()[self.POSITION_FIELD])
        self.assertEqual(str(self.UPDATED_SALARY), response.json()[self.SALARY_FIELD])
        self.assertEqual(self.company.id, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_salary_with_negative_value__expect_bad_request(self):
        expected_info_messages = ['The minimum wage is 500 USD']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.SALARY_FIELD: -45}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_salary_with_less_than_min_wage_value__expect_bad_request(self):
        expected_info_messages = ['The minimum wage is 500 USD']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.SALARY_FIELD: self.TOO_LOW_SALARY}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_salary_with_too_high_value__expect_bad_request(self):
        expected_info_messages = ['Ensure that there are no more than 7 digits in total.']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.SALARY_FIELD: self.TOO_HIGH_SALARY}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_salary_with_text__expect_bad_request(self):
        expected_info_messages = ['A valid number is required.']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.SALARY_FIELD: self.VALID_FIRST_NAME}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_company_id_with_invalid_id__expect_bad_request(self):
        expected_info_messages = ['Invalid pk "5" - object does not exist.']

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.COMPANY_ID_FIELD: 5}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete__when_pk_exists__expect_to_delete_employee_with_pk(self):
        expected_info_message = 'Not found.'

        response = self.client.delete(reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': 1}))

        self.assertEqual(expected_info_message, response.json()['detail'])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete__when_pk_does_not_exists__expect_not_found(self):
        expected_employees_count = 0

        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.delete(reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}))

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(self.EMPLOYEE_MODEL.objects.all().count(), expected_employees_count)

    def test_delete__when_delete_company_with_pk_equal_to_employee_company_id__expect_to_delete_employee_too(self):
        expected_employees_count = 0

        company_id = self.company.id
        self.COMPANY_MODEL.objects.filter(pk=company_id).delete()

        self.assertEqual(expected_employees_count, self.EMPLOYEE_MODEL.objects.all().count())
