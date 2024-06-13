from django.db import models

# Create your models here.


class Author(models.Model):
    '''
    Represents an author who creates posters.

    Parameters:
    name = name of the author

    PrimaryKey for the author is set a ForeignKey for the Poster model.
    '''
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Poster(models.Model):
    '''
    Represents a poster in the application.

    Parameters:
    title = name of the poster
    body = content of the poster
    created_on = date and time the poster was created
    author = name of the author, ForeignKey to the Author model
    priority = poster priority

    'PRIORITY_CHOICES' is a list of available priorities for posters,
    and are used in PosterForm radio buttons.

    When an object is printed, __str__() will return the title of the
    poster.
    '''
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]
    title = models.CharField(max_length=150)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default=LOW)

    def __str__(self):
        return self.title