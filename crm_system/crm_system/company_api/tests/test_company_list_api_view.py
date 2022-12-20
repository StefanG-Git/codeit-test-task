from rest_framework import status

from crm_system.common.utils import create_image
from crm_system.company_api.tests.common_company_test_config import CompanyAPIViewTestCase


class TestCompanyListAPIView(CompanyAPIViewTestCase):
    REQUIRED_FIELD_MESSAGE = ['This field is required.']
    NO_FILE_MESSAGE = ['No file was submitted.']
    COMPANY_EXISTS_MESSAGE = ['company with this name already exists.']

    def test_get__when_there_are_no_companies__expect_empty_list(self):
        response = self.client.get(self.COMPANY_LIST_URL_NAME)

        self.assertListEqual([], response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get__when_there_are_companies__expect_to_get_all(self):
        # Create company before get request
        self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        response = self.client.get(self.COMPANY_LIST_URL_NAME)

        self.assertEqual(self.VALID_NAME, response.json()[0][self.NAME_FIELD])
        self.assertEqual('/' + self.TEST_LOGO_TO_DELETE_PATH, response.json()[0][self.LOGO_FIELD])
        self.assertEqual(self.VALID_DESCRIPTION, response.json()[0][self.DESCRIPTION_FIELD])
        self.assertEqual(1, len(response.json()))
        self.assertEqual(1, self.COMPANY_MODEL.objects.all().count())
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_post__when_all_data_is_valid__expect_to_create_new_company(self):
        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(self.VALID_NAME, response.json()[self.NAME_FIELD])
        self.assertEqual('/' + self.TEST_LOGO_TO_DELETE_PATH, response.json()[self.LOGO_FIELD])
        self.assertEqual(self.VALID_DESCRIPTION, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, self.COMPANY_MODEL.objects.all().count())

    def test_post__when_missing_name_value__expect_bad_request(self):
        # Remove name value before post request
        self.valid_test_data.pop(self.NAME_FIELD)

        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.REQUIRED_FIELD_MESSAGE, response.json()[self.NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_logo_value__expect_bad_request(self):
        # Remove logo value before post request
        self.valid_test_data.pop(self.LOGO_FIELD)

        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.NO_FILE_MESSAGE, response.json()[self.LOGO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_description_value__expect_bad_request(self):
        # Remove description value before post request
        self.valid_test_data.pop(self.DESCRIPTION_FIELD)

        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.REQUIRED_FIELD_MESSAGE, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_name_is_empty_str__expect_bad_request(self):
        # Change name value to empty string before post request
        self.valid_test_data[self.NAME_FIELD] = ''

        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.BLANK_FIELD_MESSAGE, response.json()[self.NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_duplicate_name__expect_bad_request(self):
        # Create company before post request
        self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        # Create company with the same name
        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.COMPANY_EXISTS_MESSAGE, response.json()[self.NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_name_is_too_long__expect_bad_request(self):
        # Change name value to too long string before post request
        self.valid_test_data[self.NAME_FIELD] = self.TOO_LONG_NAME

        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.MAX_30_CHARS_MESSAGE, response.json()[self.NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_logo_value_is_not_a_file__expect_bad_request(self):
        # Change logo value to not a path string before post request
        self.valid_test_data[self.LOGO_FIELD] = self.TOO_LONG_NAME

        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.INVALID_FILE_FORMAT_MESSAGE, response.json()[self.LOGO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_logo_file_is_too_big__expect_bad_request(self):
        # Creating logo with size greater than acceptable
        big_image = create_image(self.TEST_LOGO_NAME, self.TOO_BIG_LOGO_PATH)
        # Change logo value to too big size before post request
        self.valid_test_data[self.LOGO_FIELD] = big_image

        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.MAX_1_MB_MESSAGE, response.json()[self.LOGO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_description_is_empty_str__expect_bad_request(self):
        # Change description value to empty string before post request
        self.valid_test_data[self.DESCRIPTION_FIELD] = ''

        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.BLANK_FIELD_MESSAGE, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_description_is_too_long__expect_bad_request(self):
        # Change description value to too long string before post request
        self.valid_test_data[self.DESCRIPTION_FIELD] = self.TOO_LONG_DESCRIPTION

        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(self.MAX_300_CHARS_MESSAGE, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
