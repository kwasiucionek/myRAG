# documents/urls.py

from django.urls import path
from .views import upload_document, search, document_list, delete_document

app_name = 'documents'

urlpatterns = [
    path('upload/', upload_document, name='upload_document'),
    path('search/', search, name='search'),
    path('document_list/', document_list, name='document_list'),
    path('delete/<int:document_id>/', delete_document, name='delete_document'),
]
