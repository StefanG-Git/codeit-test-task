from django.urls import reverse
from rest_framework import status

from crm_system.common.utils import delete_file, create_image
from crm_system.company_api.tests.common_company_test_config import CompanyAPIViewTestCase


class TestCompanyDetailAPIView(CompanyAPIViewTestCase):
    COMPANY_DETAIL_URL_NAME = 'company details'

    UPDATED_NAME = 'Updated Test Company'
    UPDATED_LOGO_PATH = 'media/for_testing/updated_valid_size_logo.png'
    UPDATED_DESCRIPTION = 'Updated test description'

    NOT_FOUND_MESSAGE = 'Not found.'

    def test_get__when_pk_does_not_exists__expect_not_found(self):
        response = self.client.get(reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': 1}))

        self.assertEqual(self.NOT_FOUND_MESSAGE, response.json()['detail'])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get__when_pk_exists__expect_to_get_company_with_pk(self):
        # Create company before get request
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        response = self.client.get(reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}))

        self.assertEqual(self.VALID_NAME, response.data[self.NAME_FIELD])
        self.assertEqual('/' + self.TEST_LOGO_TO_DELETE_PATH, response.json()[self.LOGO_FIELD])
        self.assertEqual(self.VALID_DESCRIPTION, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_does_not_exists__expect_not_found(self):
        response = self.client.put(reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': 1}))

        self.assertEqual(self.NOT_FOUND_MESSAGE, response.json()['detail'])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_put__when_pk_exists_and_update_all_fields_with_valid_data__expect_to_update_all_company_fields(self):
        # Create company before put request
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        # Change every value of the fields with new one
        updated_logo = create_image(self.TEST_LOGO_NAME, self.UPDATED_LOGO_PATH)
        updated_test_data = {
            self.NAME_FIELD: self.UPDATED_NAME,
            self.LOGO_FIELD: updated_logo,
            self.DESCRIPTION_FIELD: self.UPDATED_DESCRIPTION,
        }
        # Delete the initial logo because it's creating new with random name
        delete_file(self.TEST_LOGO_TO_DELETE_PATH)

        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data=updated_test_data
        )

        self.assertEqual(self.UPDATED_NAME, response.data[self.NAME_FIELD])
        self.assertEqual('/' + self.TEST_LOGO_TO_DELETE_PATH, response.json()[self.LOGO_FIELD])
        self.assertEqual(self.UPDATED_DESCRIPTION, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_name_with_valid_data__expect_to_update_name_only(self):
        # Create company before put request
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        # Change name value with new one
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.NAME_FIELD: self.UPDATED_NAME}
        )

        self.assertEqual(self.UPDATED_NAME, response.data[self.NAME_FIELD])
        self.assertEqual('/' + self.TEST_LOGO_TO_DELETE_PATH, response.json()[self.LOGO_FIELD])
        self.assertEqual(self.VALID_DESCRIPTION, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_name_with_empty_str__expect_bad_request(self):
        # Create company before put request
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        # Change name value to empty string
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.NAME_FIELD: ''}
        )

        self.assertListEqual(self.BLANK_FIELD_MESSAGE, response.json()[self.NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_name_with_too_long_value__expect_bad_request(self):
        # Create company before put request
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        # Change name value to too long string
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.NAME_FIELD: self.TOO_LONG_NAME}
        )

        self.assertListEqual(self.MAX_30_CHARS_MESSAGE, response.json()[self.NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_logo_with_valid_value__expect_to_update_logo_only(self):
        # Create company before put request
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        # Create new logo
        updated_logo = create_image(self.TEST_LOGO_NAME, self.UPDATED_LOGO_PATH)
        # Delete the initial logo because it's creating new with random name
        delete_file(self.TEST_LOGO_TO_DELETE_PATH)
        # Change logo value with the new one
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LOGO_FIELD: updated_logo}
        )

        self.assertEqual(self.VALID_NAME, response.data[self.NAME_FIELD])
        self.assertEqual('/' + self.TEST_LOGO_TO_DELETE_PATH, response.json()[self.LOGO_FIELD])
        self.assertEqual(self.VALID_DESCRIPTION, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_logo_with_too_big_file__expect_bad_request(self):
        # Create company before put request
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        # Create new logo with size greater than acceptable
        updated_logo = create_image(self.TEST_LOGO_NAME, self.TOO_BIG_LOGO_PATH)
        # Change logo value with the new one
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LOGO_FIELD: updated_logo}
        )

        self.assertListEqual(self.MAX_1_MB_MESSAGE, response.json()[self.LOGO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_logo_with_not_a_file_value__expect_bad_request(self):
        # Create company before put request
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        # Change logo value with string
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LOGO_FIELD: self.NAME_FIELD}
        )

        self.assertListEqual(self.INVALID_FILE_FORMAT_MESSAGE, response.json()[self.LOGO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_description_with_valid_value__expect_to_update_description_only(self):
        # Create company before put request
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        # Change name value with new one
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DESCRIPTION_FIELD: self.UPDATED_DESCRIPTION}
        )

        self.assertEqual(self.VALID_NAME, response.data[self.NAME_FIELD])
        self.assertEqual('/' + self.TEST_LOGO_TO_DELETE_PATH, response.json()[self.LOGO_FIELD])
        self.assertEqual(self.UPDATED_DESCRIPTION, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_description_with_empty_str__expect_bad_request(self):
        # Create company before put request
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        # Change description value to empty string
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DESCRIPTION_FIELD: ''}
        )

        self.assertListEqual(self.BLANK_FIELD_MESSAGE, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_description_with_too_long_value__expect_bad_request(self):
        # Create company before put request
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        # Change description value to too long string
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DESCRIPTION_FIELD: self.TOO_LONG_DESCRIPTION}
        )

        self.assertListEqual(self.MAX_300_CHARS_MESSAGE, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete__when_pk_does_not_exists__expect_not_found(self):
        response = self.client.delete(reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': 1}))

        self.assertEqual(self.NOT_FOUND_MESSAGE, response.json()['detail'])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete__when_pk_exists__expect_to_delete_company_with_pk(self):
        # Create company before put request
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        response = self.client.delete(reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}))

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, self.COMPANY_MODEL.objects.all().count())
