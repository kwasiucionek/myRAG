
# myRAG

## Opis Projektu

**myRAG** to aplikacja webowa umożliwiająca dodawanie własnych dokumentów do bazy danych oraz generowanie odpowiedzi na podstawie zawartości tych dokumentów przy użyciu modelu językowego. Projekt został zaprojektowany z myślą o łatwości użycia, estetyce oraz funkcjonalności. Wykorzystuje technologie takie jak **Celery** i **CeleryBeat** do zarządzania zadaniami asynchronicznymi, **Redis** do cachowania oraz **PostgreSQL** z rozszerzeniem **pgvector** do przechowywania danych.

### Funkcje

- **Dodawanie dokumentów:** Użytkownicy mogą dodawać własne dokumenty do bazy danych.
- **Generowanie odpowiedzi:** Na podstawie dodanych dokumentów aplikacja generuje odpowiedzi, korzystając z zaawansowanego modelu językowego.
- **Logowanie przez social media:** Użytkownicy mogą logować się za pomocą kont w mediach społecznościowych.
- **Dwustopniowe uwierzytelnianie:** Planowane wsparcie dla Two Factor Authentication (2FA) dla zwiększenia bezpieczeństwa.
- **Zaawansowany panel administracyjny:** Aplikacja oferuje rozbudowany panel administracyjny z możliwością zmiany stylizacji, oparty na **django-jazzmin**.

## Użyte Technologie

### Backend
- **Django**: framework sieciowy wysokiego poziomu w języku Python.
- **Django REST Framework**: potężny i elastyczny zestaw narzędzi do tworzenia internetowych interfejsów API.
- **Celery & Celery Beat**: Systemy kolejkowania zadań i harmonogramu.
- **Redis**: Szybki magazyn danych w pamięci używany do cachowania.
- **PostgreSQL z pgvector**: Relacyjna baza danych z wsparciem dla wektorów.
- **Django Jazzmin**: Rozbudowany i estetyczny panel administracyjny.

### Przetwarzanie i analiza tekstu
- **spaCy**: Zaawansowana biblioteka do przetwarzania języka naturalnego, używana do lematyzacji i tokenizacji tekstu.
- **NLTK**: Zestaw narzędzi do przetwarzania języka naturalnego, wykorzystywany do tokenizacji i usuwania stop words.
- **SentenceTransformer**: Model do wektoryzacji tekstu, używany do reprezentacji semantycznej dokumentów.
- **OpenAI API**: Interfejs API do generowania odpowiedzi na podstawie zawartości dokumentów.
- **TfidfVectorizer**: Technika do przekształcania tekstu na reprezentację liczbową, używana do porównywania dokumentów.
- **XLM-RoBERTa**: Model do przetwarzania sekwencji tekstowych, używany do fine-tuningu i klasyfikacji tekstu.

### Narzędzia do pracy z plikami
- **PyMuPDF**: Biblioteka do pracy z plikami PDF, używana do ekstrakcji tekstu.
- **python-docx**: Biblioteka do pracy z plikami DOCX.
- **pypandoc**: Narzędzie do konwersji dokumentów między różnymi formatami.


## Instalacja

1. **Klonowanie repozytorium:**

   ```sh
   git clone https://github.com/kwasiucionek/myRAG.git
   ```

2. **Instalacja zależności:**

   ```sh
   pip install -r requirements.txt
   python -m spacy download pl_core_news_sm
   ```

3. **Migracja bazy danych:**

   ```sh
   python manage.py migrate
   ```

4. **Uruchomienie serwera deweloperskiego:**

   ```sh
   python manage.py runserver
   ```

## MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

