from rest_framework import serializers
from .models import Company
from authenticate.models import User



class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'inn', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, attrs):
        user = self.context['request'].user
        if hasattr(user, 'owned_company'):
            raise serializers.ValidationError("Вы уже владеете компанией")
        return attrs


class CompanyAddEmployeeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким id не существует")

        if hasattr(user, 'company') and user.company is not None:
            raise serializers.ValidationError("Этот пользователь уже привязан к компании")
        return value