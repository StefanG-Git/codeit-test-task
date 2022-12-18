from rest_framework import serializers

from crm_system.common.utils import image_size_is_valid
from crm_system.company_api.models import Company


class CompanySerializer(serializers.ModelSerializer):
    LOGO_MAX_SIZE_IN_MB = 1

    class Meta:
        model = Company
        fields = '__all__'

    def validate_logo(self, image):
        if not image_size_is_valid(image, self.LOGO_MAX_SIZE_IN_MB):
            raise serializers.ValidationError(f'Max file size is {self.LOGO_MAX_SIZE_IN_MB}MB')

        return image
