from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.generics import ListCreateAPIView, CreateAPIView, \
    RetrieveUpdateAPIView

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, MeasurementSerializer


def index(request):
    return redirect(reverse('sensors'))


class SensorListCreateView(ListCreateAPIView):
    queryset = Sensor.objects.values()
    serializer_class = SensorSerializer


class SensorRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class MeasurementCreateView(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
