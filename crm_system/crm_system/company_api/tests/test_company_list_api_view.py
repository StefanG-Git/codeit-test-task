from rest_framework import status

from crm_system.common.utils import create_image
from crm_system.company_api.tests.common_company_test_config import CompanyAPIViewTestCase


class TestCompanyListAPIView(CompanyAPIViewTestCase):
    def test_get__when_there_are_no_companies__expect_empty_list(self):
        expected_companies = []

        response = self.client.get(self.COMPANY_LIST_URL_NAME)

        self.assertListEqual(expected_companies, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get__when_there_are_companies__expect_to_get_all(self):
        expected_companies_count = 1

        self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.get(self.COMPANY_LIST_URL_NAME)

        self.assertEqual(self.VALID_NAME, response.json()[0][self.NAME_FIELD])
        self.assertEqual('/' + self.TEST_LOGO_TO_DELETE_PATH, response.json()[0][self.LOGO_FIELD])
        self.assertEqual(self.VALID_DESCRIPTION, response.json()[0][self.DESCRIPTION_FIELD])
        self.assertEqual(expected_companies_count, len(response.json()))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_post__when_all_data_is_valid__expect_to_create_new_company(self):
        expected_companies_count = 1

        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertEqual(self.VALID_NAME, response.json()[self.NAME_FIELD])
        self.assertEqual('/' + self.TEST_LOGO_TO_DELETE_PATH, response.json()[self.LOGO_FIELD])
        self.assertEqual(self.VALID_DESCRIPTION, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(self.COMPANY_MODEL.objects.all().count(), expected_companies_count)

    def test_post__when_missing_name_value__expect_bad_request(self):
        expected_info_messages = ['This field is required.']

        self.valid_test_data.pop(self.NAME_FIELD)
        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_logo_value__expect_bad_request(self):
        expected_info_messages = ['No file was submitted.']

        self.valid_test_data.pop(self.LOGO_FIELD)
        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.LOGO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_missing_description_value__expect_bad_request(self):
        expected_info_messages = ['This field is required.']

        self.valid_test_data.pop(self.DESCRIPTION_FIELD)
        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_name_is_empty_str__expect_bad_request(self):
        expected_info_messages = ['This field may not be blank.']

        self.valid_test_data[self.NAME_FIELD] = ''
        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_duplicate_name__expect_bad_request(self):
        expected_info_messages = ['company with this name already exists.']

        self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_name_is_too_long__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has no more than 30 characters.']

        self.valid_test_data[self.NAME_FIELD] = self.TOO_LONG_NAME
        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_logo_value_is_not_a_file__expect_bad_request(self):
        expected_info_messages = ['The submitted data was not a file. Check the encoding type on the form.']

        self.valid_test_data[self.LOGO_FIELD] = self.TOO_LONG_NAME
        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.LOGO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_logo_file_is_too_big__expect_bad_request(self):
        expected_info_messages = ['Max file size is 1MB']

        big_image = create_image(self.TEST_LOGO_NAME, self.TOO_BIG_LOGO_PATH)
        self.valid_test_data[self.LOGO_FIELD] = big_image
        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.LOGO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_description_is_empty_str__expect_bad_request(self):
        expected_info_messages = ['This field may not be blank.']

        self.valid_test_data[self.DESCRIPTION_FIELD] = ''
        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post__when_description_is_too_long__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has no more than 300 characters.']

        self.valid_test_data[self.DESCRIPTION_FIELD] = self.TOO_LONG_DESCRIPTION
        response = self.client.post(path=self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        self.assertListEqual(expected_info_messages, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
