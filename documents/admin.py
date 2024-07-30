from django.contrib import admin
from .models import Document, DocumentVector



class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('content', 'created_at')  # Pole content i created_at jako readonly
    fields = ('title', 'file', 'content', 'created_at')  # Dodane pole file

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            file = form.cleaned_data.get('file')
            if file:
                obj.content = extract_text(file)
            obj.save()

admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentVector)
