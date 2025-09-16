from rest_framework import serializers
from .models import Storage

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['id', 'address', 'company', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_company(self, value):
        user = self.context['request'].user
        if not hasattr(user, 'company') or value != user.company:
            raise serializers.ValidationError("Вы не можете управлять этим складом.")
        return value