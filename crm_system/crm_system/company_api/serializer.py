from rest_framework import serializers

from crm_system.company_api.models import Company


class CompanySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()

    def create(self, data):
        return Company.objects.create(**data)
