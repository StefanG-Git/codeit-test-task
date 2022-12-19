from rest_framework import status

from crm_system.common.utils import create_image
from crm_system.employee_api.tests.common_employee_test_config import EmployeeAPIViewTestCase


class TestEmployeeListAPIView(EmployeeAPIViewTestCase):
    def test_get__when_there_are_no_employees__expect_empty_list(self):
        expected_employees = []

        response = self.client.get(self.EMPLOYEE_LIST_URL_NAME)

        self.assertListEqual(expected_employees, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get__when_there_are_employees__expect_to_get_all(self):
        expected_employees_count = 1

        self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.get(self.EMPLOYEE_LIST_URL_NAME)

        self.assertEqual(self.VALID_FIRST_NAME, response.json()[0][self.FIRST_NAME_FIELD])
        self.assertEqual(self.VALID_LAST_NAME, response.json()[0][self.LAST_NAME_FIELD])
        self.assertEqual(self.VALID_DATE_OF_BIRTH, response.json()[0][self.DATE_OF_BIRTH_FIELD])
        self.assertEqual('/' + self.TEST_PHOTO_TO_DELETE_PATH, response.json()[0][self.PHOTO_FIELD])
        self.assertEqual(self.VALID_POSITION, response.json()[0][self.POSITION_FIELD])
        self.assertEqual(str(self.VALID_SALARY), response.json()[0][self.SALARY_FIELD])
        self.assertEqual(self.company.id, response.json()[0][self.COMPANY_ID_FIELD])

        self.assertEqual(expected_employees_count, len(response.json()))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_post__when_all_data_is_valid__expect_to_create_new_employee(self):
        expected_employees_count = 1

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(self.VALID_FIRST_NAME, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(self.VALID_LAST_NAME, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(self.VALID_DATE_OF_BIRTH, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual('/' + self.TEST_PHOTO_TO_DELETE_PATH, response.json()[self.PHOTO_FIELD])
        self.assertEqual(self.VALID_POSITION, response.json()[self.POSITION_FIELD])
        self.assertEqual(str(self.VALID_SALARY), response.json()[self.SALARY_FIELD])
        self.assertEqual(self.company.id, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.EMPLOYEE_MODEL.objects.all().count(), expected_employees_count)

    def test_post__when_missing_first_name_value__expect_bad_request(self):
        expected_info_messages = ['This field is required.']

        self.valid_test_data.pop(self.FIRST_NAME_FIELD)
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_last_name_value__expect_bad_request(self):
        expected_info_messages = ['This field is required.']

        self.valid_test_data.pop(self.LAST_NAME_FIELD)
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_date_of_birth_value__expect_bad_request(self):
        expected_info_messages = ['This field is required.']

        self.valid_test_data.pop(self.DATE_OF_BIRTH_FIELD)
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_photo_value__expect_bad_request(self):
        expected_info_messages = ['No file was submitted.']

        self.valid_test_data.pop(self.PHOTO_FIELD)
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.PHOTO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_position_value__expect_bad_request(self):
        expected_info_messages = ['This field is required.']

        self.valid_test_data.pop(self.POSITION_FIELD)
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.POSITION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_salary_value__expect_bad_request(self):
        expected_info_messages = ['This field is required.']

        self.valid_test_data.pop(self.SALARY_FIELD)
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_company_id_value__expect_bad_request(self):
        expected_info_messages = ['This field is required.']

        self.valid_test_data.pop(self.COMPANY_ID_FIELD)
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_first_name_is_lower_case__expect_to_be_capitalized(self):
        self.valid_test_data[self.FIRST_NAME_FIELD] = self.VALID_FIRST_NAME.lower()
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(self.VALID_FIRST_NAME, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post__when_first_name_is_empty_str__expect_bad_request(self):
        expected_info_messages = ['This field may not be blank.']

        self.valid_test_data[self.FIRST_NAME_FIELD] = ''
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_first_name_is_1_letter_only__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has at least 2 characters.']

        self.valid_test_data[self.FIRST_NAME_FIELD] = 'S'
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_first_name_is_too_long__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has no more than 30 characters.']

        self.valid_test_data[self.FIRST_NAME_FIELD] = self.TOO_LONG_NAME
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_first_name_contains_digits__expect_bad_request(self):
        expected_info_messages = ['First name must contains only letters']

        self.valid_test_data[self.FIRST_NAME_FIELD] += '55'
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_first_name_contains_symbols_expect_bad_request(self):
        expected_info_messages = ['First name must contains only letters']

        self.valid_test_data[self.FIRST_NAME_FIELD] += '@%'
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_last_name_is_lower_case__expect_to_be_capitalized(self):
        self.valid_test_data[self.LAST_NAME_FIELD] = self.VALID_LAST_NAME.lower()
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(self.VALID_LAST_NAME, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post__when_last_name_is_empty_str__expect_bad_request(self):
        expected_info_messages = ['This field may not be blank.']

        self.valid_test_data[self.LAST_NAME_FIELD] = ''
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_last_name_is_1_letter_only__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has at least 2 characters.']

        self.valid_test_data[self.LAST_NAME_FIELD] = 'S'
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_last_name_is_too_long__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has no more than 30 characters.']

        self.valid_test_data[self.LAST_NAME_FIELD] = self.TOO_LONG_NAME
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_last_name_contains_digits__expect_bad_request(self):
        expected_info_messages = ['Last name must contains only letters']

        self.valid_test_data[self.LAST_NAME_FIELD] += '55'
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_name_contains_symbols__expect_bad_request(self):
        expected_info_messages = ['Last name must contains only letters']

        self.valid_test_data[self.LAST_NAME_FIELD] += '@%'
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_date_is_invalid_format__expect_bad_request(self):
        expected_info_messages = ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']

        self.valid_test_data[self.DATE_OF_BIRTH_FIELD] = self.INVALID_DATE_FORMAT
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(expected_info_messages, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_is_given_future_date__expect_bad_request(self):
        expected_info_messages = ['Invalid date']

        self.valid_test_data[self.DATE_OF_BIRTH_FIELD] = self.FUTURE_DATE
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(expected_info_messages, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_employee_is_under_18__expect_bad_request(self):
        expected_info_messages = ['People under age of 18 cannot work']

        self.valid_test_data[self.DATE_OF_BIRTH_FIELD] = self.UNDER_18_YEARS_DATE
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(expected_info_messages, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_employee_is_above_65__expect_bad_request(self):
        expected_info_messages = ['People older than 65 cannot work']

        self.valid_test_data[self.DATE_OF_BIRTH_FIELD] = self.ABOVE_65_YEARS_DATE
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(expected_info_messages, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_photo_value_is_not_a_file__expect_bad_request(self):
        expected_info_messages = ['The submitted data was not a file. Check the encoding type on the form.']

        self.valid_test_data[self.PHOTO_FIELD] = self.TOO_LONG_NAME
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.PHOTO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_photo_file_is_too_big__expect_bad_request(self):
        expected_info_messages = ['Max file size is 1MB']

        big_image = create_image(self.TEST_LOGO_NAME, self.TOO_BIG_PHOTO_PATH)
        self.valid_test_data[self.PHOTO_FIELD] = big_image
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.PHOTO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_position_is_empty_str__expect_bad_request(self):
        expected_info_messages = ['This field may not be blank.']

        self.valid_test_data[self.POSITION_FIELD] = ''
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.POSITION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_position_is_less_than_3_letter_long__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has at least 3 characters.']

        self.valid_test_data[self.POSITION_FIELD] = self.TOO_SHORT_POSITION
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.POSITION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_position_is_too_long__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has no more than 50 characters.']

        self.valid_test_data[self.POSITION_FIELD] = self.TOO_LONG_POSITION
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.POSITION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_salary_is_negative__expect_bad_request(self):
        expected_info_messages = ['The minimum wage is 500 USD']

        self.valid_test_data[self.SALARY_FIELD] = -5
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_salary_is_under_min_wave__expect_bad_request(self):
        expected_info_messages = ['The minimum wage is 500 USD']

        self.valid_test_data[self.SALARY_FIELD] = self.TOO_LOW_SALARY
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_salary_is_too_high__expect_bad_request(self):
        expected_info_messages = ['Ensure that there are no more than 7 digits in total.']

        self.valid_test_data[self.SALARY_FIELD] = self.TOO_HIGH_SALARY
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_salary_is_text__expect_bad_request(self):
        expected_info_messages = ['A valid number is required.']

        self.valid_test_data[self.SALARY_FIELD] = self.FIRST_NAME_FIELD
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_invalid_company_id__expect_bad_request(self):
        expected_info_messages = ['Invalid pk "5" - object does not exist.']

        self.valid_test_data[self.COMPANY_ID_FIELD] = 5
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)