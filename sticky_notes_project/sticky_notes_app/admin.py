from django.contrib import admin
from .models import Poster, Author

# Register your models here.

# Register Poster model
admin.site.register(Poster)

# Register Author model
admin.site.register(Author)