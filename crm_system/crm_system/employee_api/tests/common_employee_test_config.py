from django.urls import reverse
from rest_framework.test import APITestCase

from crm_system.common.utils import delete_file, create_image
from crm_system.company_api.models import Company
from crm_system.employee_api.models import Employee


class EmployeeAPIViewTestCase(APITestCase):
    EMPLOYEE_LIST_URL_NAME = reverse('employee list')

    EMPLOYEE_MODEL = Employee
    COMPANY_MODEL = Company

    FIRST_NAME_FIELD = 'first_name'
    LAST_NAME_FIELD = 'last_name'
    DATE_OF_BIRTH_FIELD = 'date_of_birth'
    PHOTO_FIELD = 'photo'
    POSITION_FIELD = 'position'
    SALARY_FIELD = 'salary'
    COMPANY_ID_FIELD = 'company_id'

    VALID_FIRST_NAME = 'Test'
    VALID_LAST_NAME = 'Testov'
    VALID_DATE_OF_BIRTH = '2000-03-15'
    VALID_SIZE_PHOTO_PATH = 'media/for_testing/valid_size_photo.png'
    VALID_POSITION = 'Testing'
    VALID_SALARY = format(2000.50, '.2f')

    TOO_LONG_NAME = VALID_FIRST_NAME * 8
    INVALID_DATE_FORMAT = '10-05-2000'
    FUTURE_DATE = '2150-10-12'
    UNDER_18_YEARS_DATE = '2020-03-01'
    ABOVE_65_YEARS_DATE = '1910-05-30'
    TOO_BIG_PHOTO_PATH = 'media/for_testing/invalid_size_image.png'
    TOO_SHORT_POSITION = 'Ss'
    TOO_LONG_POSITION = VALID_POSITION * 8
    TOO_LOW_SALARY = 250
    TOO_HIGH_SALARY = 54354353

    TEST_PHOTO_NAME = 'test_photo.png'
    TEST_PHOTO_TO_DELETE_PATH = 'media/employee_photos/' + TEST_PHOTO_NAME

    COMPANY_NAME_FIELD = 'name'
    COMPANY_LOGO_FIELD = 'logo'
    COMPANY_DESCRIPTION_FIELD = 'description'

    VALID_COMPANY_NAME = 'Valid Test Company'
    VALID_COMPANY_SIZE_LOGO_PATH = 'media/for_testing/valid_size_logo.png'
    VALID_COMPANY_DESCRIPTION = 'Valid test description'

    TEST_LOGO_NAME = 'test_logo.png'
    TEST_LOGO_TO_DELETE_PATH = 'media/company_logos/' + TEST_LOGO_NAME

    def setUp(self):
        # Create company before each test
        logo = create_image(self.TEST_LOGO_NAME, self.VALID_COMPANY_SIZE_LOGO_PATH)
        self.company = Company.objects.create(**{
            self.COMPANY_NAME_FIELD: self.VALID_COMPANY_NAME,
            self.COMPANY_LOGO_FIELD: logo,
            self.COMPANY_DESCRIPTION_FIELD: self.VALID_COMPANY_DESCRIPTION,
        })
        # Create data with valid values for each test
        photo = create_image(self.TEST_PHOTO_NAME, self.VALID_SIZE_PHOTO_PATH)
        self.valid_test_data = {
            self.FIRST_NAME_FIELD: self.VALID_FIRST_NAME,
            self.LAST_NAME_FIELD: self.VALID_LAST_NAME,
            self.DATE_OF_BIRTH_FIELD: self.VALID_DATE_OF_BIRTH,
            self.PHOTO_FIELD: photo,
            self.POSITION_FIELD: self.VALID_POSITION,
            self.SALARY_FIELD: self.VALID_SALARY,
            self.COMPANY_ID_FIELD: self.company.id
        }

    def tearDown(self):
        # Remove the images created during the test
        delete_file(self.TEST_LOGO_TO_DELETE_PATH)
        delete_file(self.TEST_PHOTO_TO_DELETE_PATH)
