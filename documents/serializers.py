from rest_framework import serializers
from .models import Document, DocumentVector

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'created_at']

class DocumentVectorSerializer(serializers.ModelSerializer):
    document = DocumentSerializer()

    class Meta:
        model = DocumentVector
        fields = ['id', 'document', 'embedding']

