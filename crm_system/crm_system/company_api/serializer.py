from rest_framework import serializers

from crm_system.company_api.models import Company


class CompanySerializer(serializers.ModelSerializer):
    LOGO_MAX_SIZE_IN_MB = 3

    class Meta:
        model = Company
        fields = '__all__'

    def validate_logo(self, image):
        if image.size > self.LOGO_MAX_SIZE_IN_MB * 1024 * 1024:
            raise serializers.ValidationError(f'Max file size is {self.LOGO_MAX_SIZE_IN_MB}MB')

        return image
