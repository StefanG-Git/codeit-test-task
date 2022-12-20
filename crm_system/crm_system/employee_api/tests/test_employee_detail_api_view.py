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

    NOT_FOUND_MESSAGE = 'Not found.'

    def test_get__when_pk_does_not_exists__expect_not_found(self):
        response = self.client.get(reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': 1}))

        self.assertEqual(self.NOT_FOUND_MESSAGE, response.json()['detail'])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get__when_pk_exists__expect_to_get_employee_with_pk(self):
        # Create employee before get request
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
        response = self.client.put(reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': 1}))

        self.assertEqual(self.NOT_FOUND_MESSAGE, response.json()['detail'])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_put__when_pk_exists_and_update_all_fields_with_valid_data__expect_to_update_all_company_fields(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change every value of the fields with new one
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
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change first name value with new one
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
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change first name value to lower case before post request
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
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change first name value to empty string
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.FIRST_NAME_FIELD: ''}
        )

        self.assertListEqual(self.BLANK_FIELD_MESSAGE, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_first_name_with_1_letter_value__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change first name value to single letter string before post request
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.FIRST_NAME_FIELD: 'J'}
        )

        self.assertListEqual(self.MIN_2_CHARS_MESSAGE, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_first_name_with_too_long_value__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change first name value to too long string before post request
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.FIRST_NAME_FIELD: self.TOO_LONG_NAME}
        )

        self.assertListEqual(self.MAX_30_CHARS_MESSAGE, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_first_name_with_digits__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change first name value that contains digits before post request
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.FIRST_NAME_FIELD: '55fdsf'}
        )

        self.assertListEqual(self.FIRST_NAME_ONLY_LETTERS_MESSAGE, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_first_name_with_symbols__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change first name value that contains symbols before post request
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.FIRST_NAME_FIELD: '$%^^fdsfs'}
        )

        self.assertListEqual(self.FIRST_NAME_ONLY_LETTERS_MESSAGE, response.json()[self.FIRST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_last_name_with_valid_data__expect_to_update_last_name_only(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change last name value with new one
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
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change last name value to lower case before post request
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
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change last name value to empty string
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LAST_NAME_FIELD: ''}
        )

        self.assertListEqual(self.BLANK_FIELD_MESSAGE, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_last_name_with_1_letter_value__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change last name value to single letter string before post request
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LAST_NAME_FIELD: 'J'}
        )

        self.assertListEqual(self.MIN_2_CHARS_MESSAGE, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_last_name_with_too_long_value__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change last name value to too long string before post request
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LAST_NAME_FIELD: self.TOO_LONG_NAME}
        )

        self.assertListEqual(self.MAX_30_CHARS_MESSAGE, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_last_name_with_digits__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change last name value that contains digits before post request
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LAST_NAME_FIELD: '55'}
        )

        self.assertListEqual(self.LAST_NAME_ONLY_LETTERS_MESSAGE, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_last_name_with_symbols__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change last name value that contains symbols before post request
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LAST_NAME_FIELD: '$%^^'}
        )

        self.assertListEqual(self.LAST_NAME_ONLY_LETTERS_MESSAGE, response.json()[self.LAST_NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_date_of_birth_with_valid_data__expect_to_update_date_of_birth_only(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change date of birth value with new one
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
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change date of birth value with invalid format date
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DATE_OF_BIRTH_FIELD: self.INVALID_DATE_FORMAT}
        )

        self.assertListEqual(self.DATE_INVALID_FORMAT_MESSAGE, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_date_of_birth_with_future_date__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change date of birth value with invalid date
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DATE_OF_BIRTH_FIELD: self.FUTURE_DATE}
        )

        self.assertListEqual(self.INVALID_DATE_MESSAGE, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_date_of_birth_with_date_less_than_18_years__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change date of birth value with less than 18 years date
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DATE_OF_BIRTH_FIELD: self.UNDER_18_YEARS_DATE}
        )

        self.assertListEqual(self.UNDER_18_YEARS_MESSAGE, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_date_of_birth_with_date_above_65_years__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change date of birth value with greater than 65 years date
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DATE_OF_BIRTH_FIELD: self.ABOVE_65_YEARS_DATE}
        )

        self.assertListEqual(self.ABOVE_65_YEARS_MESSAGE, response.json()[self.DATE_OF_BIRTH_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_photo_valid_data__expect_to_update_photo_only(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Create new photo
        updated_image = create_image(self.TEST_PHOTO_NAME, self.UPDATED_PHOTO_PATH)
        # Delete the initial photo because it's creating new with random name
        delete_file(self.TEST_PHOTO_TO_DELETE_PATH)
        # Change photo value with the new one
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
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change photo value to invalid path
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.PHOTO_FIELD: self.TOO_LONG_NAME}
        )

        self.assertListEqual(self.INVALID_FILE_FORMAT_MESSAGE, response.json()[self.PHOTO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_photo_with_too_big_file__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Create new photo with size greater than acceptable
        updated_photo = create_image(self.TEST_LOGO_NAME, self.TOO_BIG_PHOTO_PATH)
        # Change photo value with the new one
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.PHOTO_FIELD: updated_photo}
        )

        self.assertListEqual(self.MAX_1_MB_MESSAGE, response.json()[self.PHOTO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_position_with_valid_data__expect_to_update_position_only(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change position value with new one
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
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change position value to empty string
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.POSITION_FIELD: ''}
        )

        self.assertListEqual(self.BLANK_FIELD_MESSAGE, response.json()[self.POSITION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_position_with_2_letter_value__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change position value to 2 letters long string
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.POSITION_FIELD: 'CE'}
        )

        self.assertListEqual(self.MIN_3_CHARS_MESSAGE, response.json()[self.POSITION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_position_with_too_long_value__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change position value to too long string
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.POSITION_FIELD: self.TOO_LONG_POSITION}
        )

        self.assertListEqual(self.MAX_50_CHARS_MESSAGE, response.json()[self.POSITION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_salary_with_valid_data__expect_to_update_salary_only(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change salary value with new one
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
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change salary value to negative number
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.SALARY_FIELD: -45}
        )

        self.assertListEqual(self.MIN_WAGE_MESSAGE, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_salary_with_less_than_min_wage_value__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change salary value to less than min wage number
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.SALARY_FIELD: self.TOO_LOW_SALARY}
        )

        self.assertListEqual(self.MIN_WAGE_MESSAGE, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_salary_with_too_high_value__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change salary value to too big number
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.SALARY_FIELD: self.TOO_HIGH_SALARY}
        )

        self.assertListEqual(self.MAX_7_DIGITS_MESSAGE, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_salary_with_text__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change salary value to text
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.SALARY_FIELD: self.VALID_FIRST_NAME}
        )

        self.assertListEqual(self.INVALID_NUMBER_MESSAGE, response.json()[self.SALARY_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_company_id_with_invalid_id__expect_bad_request(self):
        # Create employee before put request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)
        # Change company_id value to invalid one
        response = self.client.put(
            reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.COMPANY_ID_FIELD: 5}
        )

        self.assertListEqual(self.INVALID_COMPANY_PK_MESSAGE, response.json()[self.COMPANY_ID_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete__when_pk_exists__expect_to_delete_employee_with_pk(self):
        # Create employee before delete request
        res = self.client.post(self.EMPLOYEE_LIST_URL_NAME, data=self.valid_test_data)

        response = self.client.delete(reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}))

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, self.EMPLOYEE_MODEL.objects.all().count())

    def test_delete__when_pk_does_not_exists__expect_not_found(self):
        response = self.client.delete(reverse(self.EMPLOYEE_DETAIL_URL_NAME, kwargs={'pk': 1}))

        self.assertEqual(self.NOT_FOUND_MESSAGE, response.json()['detail'])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete__when_delete_company_with_pk_equal_to_employee_company_id__expect_to_delete_employee_too(self):
        company_id = self.company.id
        self.COMPANY_MODEL.objects.filter(pk=company_id).delete()

        self.assertEqual(0, self.EMPLOYEE_MODEL.objects.all().count())
