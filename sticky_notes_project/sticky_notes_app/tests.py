from django.test import TestCase
from django.urls import reverse
from .models import Poster, Author
from .forms import PosterForm

# Create your tests here.

class TestPosterModel(TestCase):

    def setUp(self):
        self.author = Author.objects.create(name="test author")
        self.poster = Poster.objects.create(title="test title",
                                            body="this is a test",
                                            author=self.author)

    def test_poster_title(self):
        poster = Poster.objects.get(id=self.poster.id)
        self.assertEqual(poster.title, "test title")

    def test_poster_body(self):
        poster = Poster.objects.get(id=self.poster.id)
        self.assertEqual(poster.body, "this is a test")

    def test_poster_author(self):
        poster = Poster.objects.get(id=self.poster.id)
        self.assertEqual(poster.author, self.author)


class TestPosterForm(TestCase):

    def setUp(self):
        self.author = Author.objects.create(name="test author")

    def test_poster_form_is_valid(self):
        form_fields = {
            'title': 'test title',
            'body': 'this is a test',
            'priority': 'Low',
            'author_name': self.author.name
        }
        form = PosterForm(data=form_fields)
        self.assertEqual(form.is_valid(), True)

    def test_poster_form_is_not_valid(self):
        form_data = {
            'title': '',
            'body': '',
            'priority': '',
            'author_name': ''
        }
        form = PosterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('body', form.errors)
        self.assertIn('priority', form.errors)
        self.assertIn('author_name', form.errors)

    def test_poster_form_saves(self):
        form_fields = {
            'title': 'test title',
            'body': 'this is a test',
            'priority': 'Low',
            'author_name': self.author.name
        }
        form = PosterForm(data=form_fields)
        self.assertEqual(form.is_valid(), True)
        
        poster = form.save()

        self.assertEqual(poster.title, 'test title')
        self.assertEqual(poster.body, 'this is a test')
        self.assertEqual(poster.priority, 'Low')
        self.assertEqual(poster.author.name, self.author.name)


class TestViews(TestCase):

    def setUp(self):
        self.author = Author.objects.create(name='test author')
        self.poster = Poster.objects.create(title='test poster',
                                            body='this is a test',
                                            author=self.author)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200) # 200 OK
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'test poster')
        self.assertContains(response, self.author)

    def test_add_poster_get(self):
        response = self.client.get(reverse('add_poster'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_poster.html')
        self.assertIsInstance(response.context['form'], PosterForm)

    def test_add_poster_post(self):
        form_fields = {
            'title': 'test title',
            'body': 'this is a test',
            'priority': 'Low',
            'author_name': self.author.name
        }
        response = self.client.post(reverse('add_poster'), form_fields)
        self.assertEqual(response.status_code, 302) # redirect
        self.assertEqual(
            Poster.objects.filter(title='test title').count(), 1
            )

    def test_view_poster_view(self):
        response = self.client.get(
            reverse('view_poster', args=[self.poster.id])
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_poster.html')
        self.assertContains(response, 'test poster')
        self.assertContains(response, 'this is a test')
        self.assertContains(response, self.author)
        
    def test_edit_poster_get(self):
        response = self.client.get(reverse('edit_poster',
                                           args=[self.poster.id]))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], PosterForm)
        self.assertContains(response, 'test poster')
        self.assertContains(response, 'this is a test')
        self.assertContains(response, self.author)

    def test_edit_poster_post(self):
        form_fields = {
            'title': 'edited title',
            'body': 'this test is edited',
            'priority': 'Low',
            'author_name': self.author.name
        }
        response = self.client.post(reverse('edit_poster',
                                            args=[self.poster.id]),
                                            form_fields)
        self.assertEqual(response.status_code, 302)
        self.poster.refresh_from_db()
        self.assertEqual(self.poster.title, 'edited title')
        self.assertEqual(self.poster.body, 'this test is edited')
        
    def test_delete_poster_view(self):
        response = self.client.post(reverse('delete_poster',
                                            args=[self.poster.id])
                                )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_poster.html')
        self.assertContains(response, 'test poster')

    def test_poster_deleted_view(self):
        response = self.client.post(reverse('poster_deleted',
                                            args=[self.poster.id])
                                )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Poster.objects.filter(id=self.poster.id).exists()
            )

    def filter_author_filter_view(self):
        response = self.client.post(
            reverse('filter_author')
            + '?author_id='
            + str(self.author.id)
            + '&action=filter')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'test poster')

    def filter_author_delete_view(self):
        response = self.client.post(
            reverse('filter_author')
            + '?author_id='
            + str(self.author.id)
            + '&action=delete')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_author.html')
        self.assertContains(response, 'test poster')

    def test_delete_author_view(self):
        response = self.client.post(
            reverse('delete_author', args=[self.author.id])
            )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Author.objects.filter(id=self.author.id).exists()
            )
