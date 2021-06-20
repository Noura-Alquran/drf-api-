from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Book
from .serializers import BookSerializer

class BooksList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BooksDetail(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
