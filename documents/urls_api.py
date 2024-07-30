from django.urls import path
from .views import (
    DocumentListCreateAPIView, DocumentRetrieveUpdateDestroyAPIView,
    DocumentVectorListCreateAPIView, DocumentVectorRetrieveUpdateDestroyAPIView,
    search_documents
)

app_name = 'documents-api'

urlpatterns = [
    path('documents/', DocumentListCreateAPIView.as_view(), name='document-list-create'),
    path('documents/<int:pk>/', DocumentRetrieveUpdateDestroyAPIView.as_view(), name='document-retrieve-update-destroy'),
    path('document-vectors/', DocumentVectorListCreateAPIView.as_view(), name='document-vector-list-create'),
    path('document-vectors/<int:pk>/', DocumentVectorRetrieveUpdateDestroyAPIView.as_view(), name='document-vector-retrieve-update-destroy'),
    path('search/', search_documents, name='search-documents'),
]
