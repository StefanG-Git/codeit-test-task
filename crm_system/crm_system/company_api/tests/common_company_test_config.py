from django.urls import reverse
from rest_framework.test import APITestCase

from crm_system.common.utils import delete_file, create_image
from crm_system.company_api.models import Company


class CompanyAPIViewTestCase(APITestCase):
    COMPANY_LIST_URL_NAME = reverse('company list')

    COMPANY_MODEL = Company

    NAME_FIELD = 'name'
    LOGO_FIELD = 'logo'
    DESCRIPTION_FIELD = 'description'

    VALID_NAME = 'Valid Test Company'
    VALID_SIZE_LOGO_PATH = 'media/for_testing/valid_size_logo.png'
    VALID_DESCRIPTION = 'Valid test description'

    TOO_LONG_NAME = VALID_NAME * 2
    TOO_BIG_LOGO_PATH = 'media/for_testing/invalid_size_image.png'
    TOO_LONG_DESCRIPTION = VALID_DESCRIPTION * 14

    TEST_LOGO_NAME = 'test_logo.png'
    TEST_LOGO_TO_DELETE_PATH = 'media/company_logos/' + TEST_LOGO_NAME

    BLANK_FIELD_MESSAGE = ['This field may not be blank.']
    MAX_30_CHARS_MESSAGE = ['Ensure this field has no more than 30 characters.']
    MAX_300_CHARS_MESSAGE = ['Ensure this field has no more than 300 characters.']
    MAX_1_MB_MESSAGE = ['Max file size is 1MB']
    INVALID_FILE_FORMAT_MESSAGE = ['The submitted data was not a file. Check the encoding type on the form.']

    def setUp(self):
        # Create data with valid values for each test
        logo = create_image(self.TEST_LOGO_NAME, self.VALID_SIZE_LOGO_PATH)
        self.valid_test_data = {
            self.NAME_FIELD: self.VALID_NAME,
            self.LOGO_FIELD: logo,
            self.DESCRIPTION_FIELD: self.VALID_DESCRIPTION,
        }

    def tearDown(self):
        # Remove the image created during the test
        delete_file(self.TEST_LOGO_TO_DELETE_PATH)
