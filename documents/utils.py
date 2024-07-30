# utils.py

import os
import subprocess
from docx import Document as DocxDocument
import pymupdf
import pypandoc
from sentence_transformers import SentenceTransformer
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification, Trainer, TrainingArguments
from openai import OpenAI
import nltk
from nltk.tokenize import word_tokenize
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

logger = logging.getLogger(__name__)

nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load('pl_core_news_sm')  # Wczytaj model SpaCy dla języka polskiego

client = OpenAI()

# Model SentenceTransformer do wektoryzacji dokumentów
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cpu')  # Ustawienie urządzenia na 'cpu'
# Lista polskich stop words
polish_stop_words = set("""
    i oraz ale albo bo chociaż czy dlatego gdy jeśli jako kiedy ponieważ że ponieważ ponieważ 
    żeby aby aż bez dlaczego do na o od po przed przy w we za nad pod między z za dla mimo mimo 
    choć mimo że nawet owszem tak nie ani nie lecz lecz więc więc lecz tylko lecz
""".split())


def preprocess_text(text):
    """Przetwarzanie wstępne tekstu."""
    doc = nlp(text)  # Przetwarzanie tekstu za pomocą SpaCy
    words = [token.lemma_.lower() for token in doc if token.is_alpha]  # Lematizacja i usuwanie znaków niealfabetycznych

    # Usuwanie przystanków
    words = [word for word in words if word not in polish_stop_words]

    return ' '.join(words)


def get_answer_from_content(query, context):
    """Generowanie odpowiedzi na podstawie kontekstu za pomocą API OpenAI."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that answers questions based on the given context."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
        ]
    )
    return response.choices[0].message.content


def extract_text(file_path):
    """Ekstrakcja tekstu z plików o różnych formatach."""
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".txt":
        return extract_text_from_txt(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".doc":
        return extract_text_from_doc(file_path)
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".rtf":
        return extract_text_from_rtf(file_path)
    else:
        raise ValueError("Unsupported file format")


def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:  # Można użyć errors="replace" zamiast errors="ignore"
        text = file.read()
    logger.info(f"Extracted text from TXT file: {text[:100]}...")  # Logowanie tylko pierwszych 100 znaków
    return text



def extract_text_from_docx(file_path):
    """Ekstrakcja tekstu z plików DOCX."""
    doc = DocxDocument(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text_from_doc(file_path):
    """Ekstrakcja tekstu z plików DOC za pomocą antiword."""
    result = subprocess.run(['antiword', file_path], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')


import pymupdf

def extract_text_from_pdf(file_path):
    """Ekstrakcja tekstu z plików PDF za pomocą PyMuPDF."""
    doc = pymupdf.open(file_path)  # Używamy pymupdf.open() do otwierania pliku PDF
    text = ""
    for page in doc:
        text += page.get_text("text")  # Używamy get_text("text") do ekstrakcji tekstu
    return text



def extract_text_from_rtf(file_path):
    """Ekstrakcja tekstu z plików RTF za pomocą pypandoc."""
    return pypandoc.convert_file(file_path, 'plain')


def vectorize_document(content):
    """Wektoryzacja dokumentu za pomocą SentenceTransformer."""
    if not content:
        return None
    return model.encode(content)


def vectorize_text(corpus):
    """Wektoryzacja tekstu za pomocą TF-IDF."""
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(corpus)
    return vectors, vectorizer


def fine_tune_transformer(train_dataset, eval_dataset):
    """Fine-tuning modelu XLM-RoBERTa."""
    model_name = "xlm-roberta-base"
    tokenizer = XLMRobertaTokenizer.from_pretrained(model_name)
    model = XLMRobertaForSequenceClassification.from_pretrained(model_name)

    def preprocess_function(examples):
        return tokenizer(examples['text'], truncation=True, padding=True)

    train_dataset = train_dataset.map(preprocess_function, batched=True)
    eval_dataset = eval_dataset.map(preprocess_function, batched=True)

    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )

    trainer.train()
    return model
