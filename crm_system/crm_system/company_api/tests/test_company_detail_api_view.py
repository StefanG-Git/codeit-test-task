from django.urls import reverse
from rest_framework import status

from crm_system.common.utils import delete_file, create_image
from crm_system.company_api.tests.common_company_test_config import CompanyAPIViewTestCase


class TestCompanyDetailAPIView(CompanyAPIViewTestCase):
    COMPANY_DETAIL_URL_NAME = 'company details'

    UPDATED_NAME = 'Updated Test Company'
    UPDATED_LOGO_PATH = 'media/for_testing/updated_valid_size_logo.png'
    UPDATED_DESCRIPTION = 'Updated test description'

    def test_get__when_pk_does_not_exists__expect_not_found(self):
        expected_info_message = 'Not found.'

        response = self.client.get(reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': 1}))

        self.assertEqual(expected_info_message, response.json()['detail'])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get__when_pk_exists__expect_to_get_company_with_pk(self):
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.get(reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}))

        self.assertEqual(self.VALID_NAME, response.data[self.NAME_FIELD])
        self.assertEqual('/' + self.TEST_LOGO_TO_DELETE_PATH, response.json()[self.LOGO_FIELD])
        self.assertEqual(self.VALID_DESCRIPTION, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_does_not_exists__expect_not_found(self):
        expected_info_message = 'Not found.'

        response = self.client.put(reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': 1}))

        self.assertEqual(expected_info_message, response.json()['detail'])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_put__when_pk_exists_and_update_all_fields_with_valid_data__expect_to_update_all_company_fields(self):
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        updated_image = create_image(self.TEST_LOGO_NAME, self.UPDATED_LOGO_PATH)
        updated_test_data = {
            self.NAME_FIELD: self.UPDATED_NAME,
            self.LOGO_FIELD: updated_image,
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
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.NAME_FIELD: self.UPDATED_NAME}
        )

        self.assertEqual(self.UPDATED_NAME, response.data[self.NAME_FIELD])
        self.assertEqual('/' + self.TEST_LOGO_TO_DELETE_PATH, response.json()[self.LOGO_FIELD])
        self.assertEqual(self.VALID_DESCRIPTION, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_name_with_empty_str__expect_bad_request(self):
        expected_info_messages = ['This field may not be blank.']

        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.NAME_FIELD: ''}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_name_with_too_long_value__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has no more than 30 characters.']

        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.NAME_FIELD: self.TOO_LONG_NAME}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.NAME_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_logo_with_valid_value__expect_to_update_logo_only(self):
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)

        updated_image = create_image(self.TEST_LOGO_NAME, self.UPDATED_LOGO_PATH)
        # Delete the initial logo because it's creating new with random name
        delete_file(self.TEST_LOGO_TO_DELETE_PATH)

        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LOGO_FIELD: updated_image}
        )

        self.assertEqual(self.VALID_NAME, response.data[self.NAME_FIELD])
        self.assertEqual('/' + self.TEST_LOGO_TO_DELETE_PATH, response.json()[self.LOGO_FIELD])
        self.assertEqual(self.VALID_DESCRIPTION, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_logo_with_too_big_file__expect_bad_request(self):
        expected_info_messages = ['Max file size is 1MB']

        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        updated_image = create_image(self.TEST_LOGO_NAME, self.TOO_BIG_LOGO_PATH)

        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LOGO_FIELD: updated_image}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.LOGO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_logo_with_not_a_file_value__expect_bad_request(self):
        expected_info_messages = ['The submitted data was not a file. Check the encoding type on the form.']

        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.LOGO_FIELD: self.NAME_FIELD}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.LOGO_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_description_with_valid_value__expect_to_update_description_only(self):
        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DESCRIPTION_FIELD: self.UPDATED_DESCRIPTION}
        )

        self.assertEqual(self.VALID_NAME, response.data[self.NAME_FIELD])
        self.assertEqual('/' + self.TEST_LOGO_TO_DELETE_PATH, response.json()[self.LOGO_FIELD])
        self.assertEqual(self.UPDATED_DESCRIPTION, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put__when_pk_exists_and_update_only_description_with_empty_str__expect_bad_request(self):
        expected_info_messages = ['This field may not be blank.']

        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DESCRIPTION_FIELD: ''}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_put__when_pk_exists_and_update_only_description_with_too_long_value__expect_bad_request(self):
        expected_info_messages = ['Ensure this field has no more than 300 characters.']

        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.put(
            reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}),
            data={self.DESCRIPTION_FIELD: self.TOO_LONG_DESCRIPTION}
        )

        self.assertListEqual(expected_info_messages, response.json()[self.DESCRIPTION_FIELD])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_delete__when_pk_does_not_exists__expect_not_found(self):
        expected_info_message = 'Not found.'

        response = self.client.delete(reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': 1}))

        self.assertEqual(expected_info_message, response.json()['detail'])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete__when_pk_exists__expect_to_delete_company_with_pk(self):
        expected_companies_count = 0

        res = self.client.post(self.COMPANY_LIST_URL_NAME, data=self.valid_test_data)
        response = self.client.delete(reverse(self.COMPANY_DETAIL_URL_NAME, kwargs={'pk': res.json()['id']}))

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(self.COMPANY_MODEL.objects.all().count(), expected_companies_count)
