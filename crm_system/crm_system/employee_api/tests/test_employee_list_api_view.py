from rest_framework import status

from crm_system.common.utils import create_image
from crm_system.employee_api.tests.common_employee_test_config import EmployeeAPIViewTestCase


class TestEmployeeListAPIView(EmployeeAPIViewTestCase):
    REQUIRED_FIELD_MESSAGE = ['This field is required.']
    NO_FILE_MESSAGE = ['No file was submitted.']

    def test_get__when_there_are_no_employees__expect_empty_list(self):
        response = self.client.get(self.EMPLOYEE_LIST_URL_NAME)

        self.assertListEqual([], response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get__when_there_are_employees__expect_to_get_all(self):
        # Create employee before get request
        self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        response = self.client.get(self.EMPLOYEE_LIST_URL_NAME)

        self.assertEqual(self.VALID_FIRST_NAME, response.json()[0][self.FIRST_NAME_FIELD])
        self.assertEqual(self.VALID_LAST_NAME, response.json()[0][self.LAST_NAME_FIELD])
        self.assertEqual(self.VALID_DATE_OF_BIRTH, response.json()[0][self.DATE_OF_BIRTH_FIELD])
        self.assertEqual('/' + self.TEST_PHOTO_TO_DELETE_PATH, response.json()[0][self.PHOTO_FIELD])
        self.assertEqual(self.VALID_POSITION, response.json()[0][self.POSITION_FIELD])
        self.assertEqual(str(self.VALID_SALARY), response.json()[0][self.SALARY_FIELD])
        self.assertEqual(self.company.id, response.json()[0][self.COMPANY_ID_FIELD])
        self.assertEqual(1, len(response.json()))
        self.assertEqual(1, self.EMPLOYEE_MODEL.objects.all().count())
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_post__when_all_data_is_valid__expect_to_create_new_employee(self):
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(self.VALID_FIRST_NAME, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(self.VALID_LAST_NAME, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(self.VALID_DATE_OF_BIRTH, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual('/' + self.TEST_PHOTO_TO_DELETE_PATH, response.json()[self.PHOTO_FIELD])
        self.assertEqual(self.VALID_POSITION, response.json()[self.POSITION_FIELD])
        self.assertEqual(str(self.VALID_SALARY), response.json()[self.SALARY_FIELD])
        self.assertEqual(self.company.id, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, self.EMPLOYEE_MODEL.objects.all().count())

    def test_post__when_missing_first_name_value__expect_bad_request(self):
        # Remove first name value before post request
        self.valid_test_data.pop(self.FIRST_NAME_FIELD)

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.REQUIRED_FIELD_MESSAGE, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_last_name_value__expect_bad_request(self):
        # Remove last name value before post request
        self.valid_test_data.pop(self.LAST_NAME_FIELD)

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.REQUIRED_FIELD_MESSAGE, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_date_of_birth_value__expect_bad_request(self):
        # Remove date of birth value before post request
        self.valid_test_data.pop(self.DATE_OF_BIRTH_FIELD)

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.REQUIRED_FIELD_MESSAGE, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_photo_value__expect_bad_request(self):
        # Remove photo value before post request
        self.valid_test_data.pop(self.PHOTO_FIELD)

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.NO_FILE_MESSAGE, response.json()[self.PHOTO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_position_value__expect_bad_request(self):
        # Remove position value before post request
        self.valid_test_data.pop(self.POSITION_FIELD)

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.REQUIRED_FIELD_MESSAGE, response.json()[self.POSITION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_salary_value__expect_bad_request(self):
        # Remove salary value before post request
        self.valid_test_data.pop(self.SALARY_FIELD)

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.REQUIRED_FIELD_MESSAGE, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_company_id_value__expect_bad_request(self):
        # Remove company id value before post request
        self.valid_test_data.pop(self.COMPANY_ID_FIELD)

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.REQUIRED_FIELD_MESSAGE, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_first_name_is_lower_case__expect_to_be_capitalized(self):
        # Change first name value to lower case before post request
        self.valid_test_data[self.FIRST_NAME_FIELD] = self.VALID_FIRST_NAME.lower()

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(self.VALID_FIRST_NAME, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post__when_first_name_is_empty_str__expect_bad_request(self):
        # Change first name value to empty string before post request
        self.valid_test_data[self.FIRST_NAME_FIELD] = ''

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.BLANK_FIELD_MESSAGE, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_first_name_is_1_letter_only__expect_bad_request(self):
        # Change first name value to single letter string before post request
        self.valid_test_data[self.FIRST_NAME_FIELD] = 'S'

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.MIN_2_CHARS_MESSAGE, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_first_name_is_too_long__expect_bad_request(self):
        # Change first name value to too long string before post request
        self.valid_test_data[self.FIRST_NAME_FIELD] = self.TOO_LONG_NAME

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.MAX_30_CHARS_MESSAGE, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_first_name_contains_digits__expect_bad_request(self):
        # Change first name value that contains digits before post request
        self.valid_test_data[self.FIRST_NAME_FIELD] += 'dsa55'

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.FIRST_NAME_ONLY_LETTERS_MESSAGE, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_first_name_contains_symbols_expect_bad_request(self):
        # Change first name value that contains symbols before post request
        self.valid_test_data[self.FIRST_NAME_FIELD] += 'fdsf@%'

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.FIRST_NAME_ONLY_LETTERS_MESSAGE, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_last_name_is_lower_case__expect_to_be_capitalized(self):
        # Change last name value to lower case before post request
        self.valid_test_data[self.LAST_NAME_FIELD] = self.VALID_LAST_NAME.lower()

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(self.VALID_LAST_NAME, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_post__when_last_name_is_empty_str__expect_bad_request(self):
        # Change last name value to empty string before post request
        self.valid_test_data[self.LAST_NAME_FIELD] = ''

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.BLANK_FIELD_MESSAGE, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_last_name_is_1_letter_only__expect_bad_request(self):
        # Change last name value to single letter string before post request
        self.valid_test_data[self.LAST_NAME_FIELD] = 'S'

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.MIN_2_CHARS_MESSAGE, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_last_name_is_too_long__expect_bad_request(self):
        # Change last name value to too long string before post request
        self.valid_test_data[self.LAST_NAME_FIELD] = self.TOO_LONG_NAME

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.MAX_30_CHARS_MESSAGE, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_last_name_contains_digits__expect_bad_request(self):
        # Change last name value that contains digits before post request
        self.valid_test_data[self.LAST_NAME_FIELD] += 'fds55'

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.LAST_NAME_ONLY_LETTERS_MESSAGE, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_last_name_contains_symbols__expect_bad_request(self):
        # Change last name value that contains symbols before post request
        self.valid_test_data[self.LAST_NAME_FIELD] += '@%fdsfs'

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.LAST_NAME_ONLY_LETTERS_MESSAGE, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_date_is_invalid_format__expect_bad_request(self):
        # Change date of birth value with invalid format date
        self.valid_test_data[self.DATE_OF_BIRTH_FIELD] = self.INVALID_DATE_FORMAT

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(self.DATE_INVALID_FORMAT_MESSAGE, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_is_given_future_date__expect_bad_request(self):
        # Change date of birth value with future date
        self.valid_test_data[self.DATE_OF_BIRTH_FIELD] = self.FUTURE_DATE

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(self.INVALID_DATE_MESSAGE, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_employee_is_under_18__expect_bad_request(self):
        # Change date of birth value with less than 18 years date
        self.valid_test_data[self.DATE_OF_BIRTH_FIELD] = self.UNDER_18_YEARS_DATE

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(self.UNDER_18_YEARS_MESSAGE, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_employee_is_above_65__expect_bad_request(self):
        # Change date of birth value with greater than 65 years date
        self.valid_test_data[self.DATE_OF_BIRTH_FIELD] = self.ABOVE_65_YEARS_DATE

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(self.ABOVE_65_YEARS_MESSAGE, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_photo_value_is_not_a_file__expect_bad_request(self):
        # Change photo value to invalid path before post request
        self.valid_test_data[self.PHOTO_FIELD] = self.TOO_LONG_NAME

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.INVALID_FILE_FORMAT_MESSAGE, response.json()[self.PHOTO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_photo_file_is_too_big__expect_bad_request(self):
        # Creating photo with size greater than acceptable
        big_image = create_image(self.TEST_LOGO_NAME, self.TOO_BIG_PHOTO_PATH)
        # Change photo value to too big size before post request
        self.valid_test_data[self.PHOTO_FIELD] = big_image

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.MAX_1_MB_MESSAGE, response.json()[self.PHOTO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_position_is_empty_str__expect_bad_request(self):
        # Change position value to empty string before post request
        self.valid_test_data[self.POSITION_FIELD] = ''

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.BLANK_FIELD_MESSAGE, response.json()[self.POSITION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_position_is_less_than_3_letter_long__expect_bad_request(self):
        # Change position value to 2 letters long string before post request
        self.valid_test_data[self.POSITION_FIELD] = self.TOO_SHORT_POSITION

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.MIN_3_CHARS_MESSAGE, response.json()[self.POSITION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_position_is_too_long__expect_bad_request(self):
        # Change position value to too long string before post request
        self.valid_test_data[self.POSITION_FIELD] = self.TOO_LONG_POSITION

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.MAX_50_CHARS_MESSAGE, response.json()[self.POSITION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_salary_is_negative_number__expect_bad_request(self):
        # Change salary value to negative number before post request
        self.valid_test_data[self.SALARY_FIELD] = -5
        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.MIN_WAGE_MESSAGE, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_salary_is_less_than_min_wage__expect_bad_request(self):
        # Change salary value to less than min wage number before post request
        self.valid_test_data[self.SALARY_FIELD] = self.TOO_LOW_SALARY

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.MIN_WAGE_MESSAGE, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_salary_is_too_high__expect_bad_request(self):
        # Change salary value to too big number before post request
        self.valid_test_data[self.SALARY_FIELD] = self.TOO_HIGH_SALARY

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.MAX_7_DIGITS_MESSAGE, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_salary_is_text__expect_bad_request(self):
        # Change salary value to text before post request
        self.valid_test_data[self.SALARY_FIELD] = self.FIRST_NAME_FIELD

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.INVALID_NUMBER_MESSAGE, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_invalid_company_id__expect_bad_request(self):
        # Change company_id value to invalid one before post request
        self.valid_test_data[self.COMPANY_ID_FIELD] = 5

        response = self.client.post(path=self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.INVALID_COMPANY_PK_MESSAGE, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)