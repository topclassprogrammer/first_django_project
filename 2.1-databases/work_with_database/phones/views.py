from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    request_param = request.GET.get('sort')
    if request_param == 'name':
        phones = Phone.objects.all().order_by('name')
    elif request_param == 'min_price':
        phones = Phone.objects.all().order_by('price')
    elif request_param == 'max_price':
        phones = Phone.objects.all().order_by('-price')
    else:
        phones = Phone.objects.all()
    template = 'catalog.html'
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    try:
        context = {'phone': Phone.objects.get(slug=slug)}
    except ObjectDoesNotExist:
        return HttpResponse(f'Телефон {slug} в каталоге не обнаружен')
    template = 'product.html'
    return render(request, template, context)
