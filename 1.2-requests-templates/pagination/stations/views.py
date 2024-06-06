import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page_number = request.GET.get('page', 1)
    with open(settings.BUS_STATION_CSV, 'r', encoding='utf-8') as f:
        content = list(csv.DictReader(f))
    paginator = Paginator(content, 10)
    page = paginator.get_page(page_number)
    context = {'page': page}
    template_name = 'stations/index.html'
    return render(request, template_name, context)
