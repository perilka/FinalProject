from rest_framework import serializers
from .models import User, Company, Storage


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CompanySerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'inn', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, attrs):
        user = self.context['request'].user
        if hasattr(user, 'company'):
            raise serializers.ValidationError("Вы уже владеете компанией")
        return attrs

class CompanyAddEmployeeSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Пользователь с таким id не существует")
        return value


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['id', 'address', 'company', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_company(self, value):
        user = self.context['request'].user
        if hasattr(user, 'company') and value != user.company:
            raise serializers.ValidationError("Вы не можете управлять этим складом.")
        return value


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
