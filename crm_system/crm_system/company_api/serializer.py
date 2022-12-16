from rest_framework import serializers

from crm_system.company_api.models import Company


class CompanySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Company
        fields = '__all__'
