from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Genre(models.Model):
    Book_genre_choice = (
     ('Fantasy', 'Fantasy'),
    ('Adventure', 'Adventure'),
    ('Romance', 'Romance'),
)
    name = models.CharField(max_length=200, choices = Book_genre_choice, help_text='Select a book genre')
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(help_text='Book reports:')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    readers = models.ManyToManyField(User, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    #date_of_birth = models.DateField(null=True, blank=True)
    #date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
'''
class Reader(models.Model):
    books = ManyToManyField(Book)
    name = model.charfield(max_length=10000)
'''
