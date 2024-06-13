from django import forms
from .models import Poster, Author

class PosterForm(forms.ModelForm):
    '''
    Form logic for poster creation or editing. Form fields are:

    title = name of the poster
    body = poster body content
    created_on = date and time the poster was created
    author = poster author / to be used for poster categorisation
    priority = set the priority attribute for the poster
    '''

    # Author field is defined separately as it is allows for displaying
    # the author's name rather than it's primary key in the database
    author_name = forms.CharField(max_length=50,
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control'}
                                      )
                                )

    class Meta:
        model = Poster
        fields = ['title', 'body', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'priority': forms.RadioSelect(attrs={'class': 'priority-selector'}),
        }

    def __init__(self, *args, **kwargs):
        '''
        Extends the ModelForm class, and allows the 'author' field of the
        form to be pre-filled of an author already exists for a poster
        instance.
        '''
        super().__init__(*args, **kwargs)
        if self.instance.author:
            self.initial['author_name'] = self.instance.author.name

    def save(self, commit=True):
        '''
        Extend the save() method to ensure the author name given in the
        form is validated, as custom form fields won't be automatically
        validated. Then, update the databases.
        '''
        instance = super().save(commit=False)
        author_name = self.cleaned_data.get('author_name')

        if author_name:
            author, created = Author.objects.get_or_create(name=author_name)
            instance.author = author
        
        if commit:
            instance.save()
        return instance
