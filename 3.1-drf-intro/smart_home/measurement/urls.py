from django.urls import path

from measurement.views import SensorListCreateView, SensorRetrieveUpdateView, \
    MeasurementCreateView

urlpatterns = [
    path('sensors/', SensorListCreateView.as_view(), name='sensors'),
    path('sensors/<pk>/', SensorRetrieveUpdateView.as_view()),
    path('measurements/', MeasurementCreateView.as_view()),
]
