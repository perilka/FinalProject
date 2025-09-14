from django.urls import path
from .views import CompanyListView, CompanyDetailView, CompanyCreateView, CompanyAddEmployeeView

urlpatterns = [
    path('', CompanyListView.as_view(), name='company-list'),
    path('create/', CompanyCreateView.as_view(), name='company-create'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('<int:pk>/add-employee/', CompanyAddEmployeeView.as_view(), name='company-add-employee'),
]

