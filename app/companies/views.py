from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .serializers import CompanySerializer, CompanyAddEmployeeSerializer
from .permissions import IsCompanyOwner, IsCompanyOwnerOrEmployee
from authenticate.models import User
from rest_framework.response import Response
from rest_framework import status, serializers
from django.db import models
from authenticate.serializers import EmployeeSerializer



@extend_schema(tags=['Компании'])
class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'owned_company'):
            raise serializers.ValidationError("Вы уже владеете компанией")
        serializer.save(owner=user)


@extend_schema(tags=['Компании'])
class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrEmployee]


@extend_schema(tags=['Компании'])
class CompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Company.objects.filter(
            models.Q(owner=user) | models.Q(id=user.company_id)
        ).distinct()


@extend_schema(tags=['Компании'])
class CompanyAddEmployeeView(generics.GenericAPIView):
    serializer_class = CompanyAddEmployeeSerializer
    permission_classes = [IsAuthenticated, IsCompanyOwner]
    queryset = Company.objects.all()
    lookup_field = 'pk'

    def post(self, request, pk):
        company = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        user = User.objects.get(id=user_id)

        if hasattr(user, 'company') and user.company is not None:
            return Response({"detail": "Этот пользователь уже привязан к компании"}, status=status.HTTP_400_BAD_REQUEST)

        user.company = company
        user.save()

        return Response({"detail": "Gjkmpjdfntkm ecgtiyj ghbrhtgkty r rjvgfybb"}, status=status.HTTP_200_OK)


@extend_schema(tags=['Компании'])
class CompanyEmployeesListView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsCompanyOwner]
    queryset = Company.objects.all()
    lookup_field = 'pk'

    def get_queryset(self):
        company = self.get_object()
        return company.employees.all()