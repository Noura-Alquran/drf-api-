from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Book

class BookModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='Noura',password='2551996')
        test_user.save()

        test_book = Book.objects.create(
            author = test_user,
            title = 'Cooking',
            description = 'something about the book'
        )
        test_book.save()

    def test_blog_content(self):
        book = Book.objects.get(id=1)
        self.assertEqual(str(book.author), 'Noura')
        self.assertEqual(book.title, 'Cooking')
        self.assertEqual(book.description, 'something about the book')

class APITest(APITestCase):
    def test_list(self):
        response = self.client.get(reverse('books_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail(self):

        test_user = get_user_model().objects.create_user(username='Noura',password='2551996')
        test_user.save()

        test_book = Book.objects.create(
            author = test_user,
            title = 'Cooking',
            description = 'something about the book'
        )
        test_book.save()

        response = self.client.get(reverse('books_detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id':1,
            'title': test_book.title,
            'description': test_book.description,
            'author': test_user.id,
        })


    def test_create(self):
        test_user = get_user_model().objects.create_user(username='Noura',password='2551996')
        test_user.save()


        url = reverse('books_list')
        data = {
            "title":"Python!!!",
            "description":"something about the book",
            "author":test_user.id,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, test_user.id)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, data['title'])

    def test_update(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_book = Book.objects.create(
            author = test_user,
            title = 'Title of Blog',
            description = 'Words about the blog'
        )

        test_book.save()

        url = reverse('books_detail',args=[test_book.id])
        data = {
            "title":"Python!!!",
            "author":test_book.author.id,
            "description":test_book.description,
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, url)

        self.assertEqual(Book.objects.count(), test_book.id)
        self.assertEqual(Book.objects.get().title, data['title'])


    def test_delete(self):
        """Test the api can delete a book."""

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_book = Book.objects.create(
            author = test_user,
            title = 'Title of Blog',
            description = 'Words about the blog'
        )

        test_book.save()

        book = Book.objects.get()
        url = reverse('books_detail', kwargs={'pk': book.id})
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, url)