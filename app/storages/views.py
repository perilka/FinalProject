from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Storage
from .serializers import StorageSerializer
from companies.permissions import IsCompanyOwner, IsCompanyOwnerOrEmployee
from rest_framework import serializers



@extend_schema(tags=['Склады'])
class StorageCreateView(generics.CreateAPIView):
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated, IsCompanyOwner]

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'company') or user.company.owner != user:
            raise serializers.ValidationError("Вы не являетесь владельцем компании")
        serializer.save(company=user.company)


@extend_schema(tags=['Склады'])
class StorageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrEmployee]


@extend_schema(tags=['Склады'])
class StorageListView(generics.ListAPIView):
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated, IsCompanyOwner]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'company') and user.company.owner == user:
            return Storage.objects.filter(company=user.company)
        return Storage.objects.none()

