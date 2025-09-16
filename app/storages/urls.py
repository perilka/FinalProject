from django.urls import path
from .views import StorageCreateView, StorageListView

urlpatterns = [
    path('', StorageListView.as_view(), name='storage-list'),
    path('create/', StorageCreateView.as_view(), name='storage-create'),
]
