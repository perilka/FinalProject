from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Company, User
from .permissions import IsCompanyOwner, IsCompanyOwnerOrEmployee
from .serializers import UserSerializer, CompanySerializer, CompanyAddEmployeeSerializer
from rest_framework import serializers

@extend_schema(tags=['Пользователи'])
class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@extend_schema(tags=['Компании'])
class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'company'):
            raise serializers.ValidationError("Пользователь уже владеет компанией")
        serializer.save(owner=user)

@extend_schema(tags=['Компании'])
class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyOwner]

@extend_schema(tags=['Компании'])
class CompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsCompanyOwnerOrEmployee]
    queryset = Company.objects.all()
    lookup_field = 'pk'


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

        if user in company.employees.all():
            return Response({"detail": "User already added"}, status=status.HTTP_400_BAD_REQUEST)

        company.employees.add(user)
        return Response({"detail": "User added successfully"}, status=status.HTTP_200_OK)
