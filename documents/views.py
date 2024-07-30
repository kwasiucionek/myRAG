from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import Document, DocumentVector
from .utils import preprocess_text, vectorize_document, get_answer_from_content, extract_text
from django.core.paginator import Paginator
from django.db.models import F
from pgvector.django import CosineDistance
from rest_framework import generics
from .serializers import DocumentSerializer, DocumentVectorSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .tasks import process_document

import logging


logger = logging.getLogger(__name__)


def redirect_to_login(request):
    return redirect('account_login')

@login_required
def upload_document(request):
    if request.method == "POST" and request.FILES['document']:
        try:
            file = request.FILES['document']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(file.name, file)
            document = Document.objects.create(title=file.name, file=file, user=request.user)
            process_document.delay(fs.path(filename), document.id)
            logger.info(f"Document uploaded and task started for document id: {document.id}")
            return redirect('documents:document_list')
        except Exception as e:
            logger.error(f"Error uploading document: {e}")
    return render(request, 'documents/upload.html')


CACHE_TTL = getattr(settings, 'CACHE_TTL', 60 * 15)

class DocumentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentVectorListCreateAPIView(generics.ListCreateAPIView):
    queryset = DocumentVector.objects.all()
    serializer_class = DocumentVectorSerializer

class DocumentVectorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentVector.objects.all()
    serializer_class = DocumentVectorSerializer

@api_view(['GET'])
def search_documents(request):
    query = request.GET.get('q')
    if not query:
        return Response({'results': [], 'message': 'Please enter a search query.'})

    cache_key = f"search_{query}"
    cache_result = cache.get(cache_key)

    if cache_result:
        return Response(cache_result)

    query_vector = vectorize_document(query)

    results = DocumentVector.objects.annotate(
        similarity=CosineDistance('embedding', query_vector)
    ).order_by('similarity')[:5]

    context = ""
    max_context_length = 30000
    current_length = 0
    max_document_length = 6000

    for result in results:
        document_title = result.document.title
        document_content = result.document.content[:max_document_length]
        document_length = len(document_title) + len(document_content) + 2

        if current_length + document_length > max_context_length:
            continue

        context += f"{document_title}\n{document_content}\n\n"
        current_length += document_length

    if len(context) == 0 and results:
        result = results[0]
        document_title = result.document.title
        document_content = result.document.content[:max_document_length]
        context += f"{document_title}\n{document_content}\n\n"

    answer = get_answer_from_content(query, context)

    serializer = DocumentVectorSerializer(results, many=True)
    cache_result = {
        'results': serializer.data,
        'query': query,
        'answer': answer
    }

    cache.set(cache_key, cache_result, timeout=CACHE_TTL)
    return Response(cache_result)
def upload_document(request):
    if request.method == "POST" and request.FILES['document']:
        file = request.FILES['document']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(file.name, file)
        document = Document.objects.create(title=file.name, file=file, user=request.user)
        process_document.delay(fs.path(filename), document.id)  # Uruchamiamy zadanie Celery
        return redirect('documents:document_list')
    return render(request, 'documents/upload.html')

def document_list(request):
    sort_param = request.GET.get('sort', '-created_at')  # Domyślnie sortuj po dacie malejąco
    query = request.GET.get('q')

    documents = Document.objects.filter(user=request.user)  # Filtrowanie dokumentów zalogowanego użytkownika

    if query:
        documents = documents.filter(title__icontains=query)

    if sort_param.startswith('-'):
        documents = documents.order_by(F(sort_param[1:]).desc(nulls_last=True))
    else:
        documents = documents.order_by(F(sort_param).asc(nulls_last=True))

    paginator = Paginator(documents, 10)  # 10 dokumentów na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'documents/document_list.html', context)

@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, user=request.user)  # Dodane filtrowanie po użytkowniku
    document.delete()
    return redirect('documents:document_list')

def search(request):
    query = request.GET.get('q')
    if not query:
        return render(request, 'documents/search.html', {'results': [], 'message': 'Please enter a search query.', 'is_popup': False})

    cache_key = f"search_{request.user.id}_{query}"
    cache_result = cache.get(cache_key)

    if cache_result:
        return render(request, 'documents/search.html', {**cache_result, 'is_popup': False})

    preprocessed_query = preprocess_text(query)
    query_vector = vectorize_document(preprocessed_query)

    results = DocumentVector.objects.filter(document__user=request.user).annotate(
        similarity=CosineDistance('embedding', query_vector)
    ).order_by('similarity')[:5]

    context = ""
    max_context_length = 3000
    current_length = 0
    max_document_length = 600

    for result in results:
        document_title = result.document.title
        document_content = result.document.content[:max_document_length]
        document_length = len(document_title) + len(document_content) + 2

        if current_length + document_length > max_context_length:
            continue

        context += f"{document_title}\n{document_content}\n\n"
        current_length += document_length

    if len(context) == 0 and results:
        result = results[0]
        document_title = result.document.title
        document_content = result.document.content[:max_document_length]
        context += f"{document_title}\n{document_content}\n\n"

    answer = get_answer_from_content(query, context)

    context_data = {
        'results': results,
        'query': query,
        'answer': answer,
        'is_popup': False
    }

    cache.set(cache_key, context_data, timeout=CACHE_TTL)
    return render(request, 'documents/search.html', context_data)
