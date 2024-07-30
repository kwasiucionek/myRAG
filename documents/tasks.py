import logging

from .models import Document, DocumentVector
from .utils import preprocess_text, vectorize_document, extract_text
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task
def process_document(file_path, document_id):
    logger.info(f"Processing document id: {document_id} with file path: {file_path}")
    try:
        content = extract_text(file_path)
        content = preprocess_text(content)
        document = Document.objects.get(id=document_id)
        document.content = content
        document.save()
        vector = vectorize_document(content)
        DocumentVector.objects.create(document=document, embedding=vector)
        logger.info(f"Document vector created for document id: {document_id}")
    except Exception as e:
        logger.error(f"Error processing document id: {document_id}: {e}")



