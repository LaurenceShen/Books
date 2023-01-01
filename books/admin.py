from django.contrib import admin

# Register your models here.
from .models import  Genre, Book, Author

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Author)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'summary', 'Genere', 'readers')
    #list_filter = ('status', 'due_back')

