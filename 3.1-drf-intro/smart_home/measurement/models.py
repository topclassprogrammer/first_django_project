from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()


class Measurement(models.Model):
    temperature = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE,
                               related_name='measurements')
