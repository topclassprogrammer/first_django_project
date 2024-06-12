import csv
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.utils.text import slugify

from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open(settings.PHONES_CSV, 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))
        for phone in phones:
            try:
                Phone.objects.create(id=phone['id'],
                                     name=phone['name'],
                                     price=phone['price'],
                                     image=phone['image'],
                                     release_date=datetime.strptime(
                                     phone['release_date'], '%Y-%m-%d'),
                                     lte_exists=phone['lte_exists'],
                                     slug=slugify(phone['name']))
            except IntegrityError:
                raise ValueError('Загружаемый первичный ключ из csv-файла '
                                 'уже присутствует в таблице БД')
