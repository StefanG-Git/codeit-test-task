from rest_framework import serializers

from crm_system.company_api.models import Company


class CompanySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()

    def create(self, data):
        return Company.objects.create(**data)

    def update(self, instance, data):
        instance.name = data.get('name', instance.name)
        instance.description = data.get('description', instance.description)

        instance.save()

        return instance