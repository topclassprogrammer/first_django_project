from django.http import HttpResponse
from django.shortcuts import render, redirect

from books.models import Book
from django.urls import reverse


def index_view(request):
    return redirect(reverse('books'))


def books_view(request):
    template = 'books/books_list.html'
    context = {'books': Book.objects.all()}
    return render(request, template, context)


# Реализация ментора
def books_pub_date(request, pub_date):
    template = 'books/books_by_date.html'
    books_objects = Book.objects.filter(pub_date=pub_date)
    print('books_objects -', books_objects)
    books_next = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date').first()
    print('books_next -', books_next)
    books_previous = Book.objects.filter(pub_date__lt=pub_date).order_by('-pub_date').first()
    print('books_previous -', books_previous)
    context = {
        'books': books_objects,
        'next_book': books_next,
        'previous_book': books_previous,
    }
    return render(request, template, context)


# Моя реализация
# def books_by_date_view(request, date):
#     dates = sorted(set([el['pub_date'] for el in Book.objects.values()]))
#     try:
#         index = dates.index(date)
#     except ValueError:
#         return HttpResponse(f'За дату {date} в каталоге ничего нет')
#     next_index = index + 1
#     previous_index = index - 1
#     if next_index in range(len(dates)):
#         next_date = dates[next_index]
#     else:
#         next_date = None
#     if previous_index in range(len(dates)):
#         previous_date = dates[previous_index]
#     else:
#         previous_date = None
#     template = 'books/books_by_date.html'
#     context = {
#         'books': Book.objects.filter(pub_date=date),
#         'next_page': next_date, 'previous_page': previous_date
#     }
#     return render(request, template, context)
