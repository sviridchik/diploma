from choices import TYPE_CHOICES, DOSE_CHOICES, FOOD_CHOICES
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from managment.models import Patient


class TimeTable(models.Model):
    time = models.TimeField(verbose_name=_("time"))
    # schedule = models.ForeignKey(Schedule, verbose_name=_('schedule'), on_delete = models.CASCADE)


class Schedule(models.Model):
    cycle_start = models.DateField(verbose_name=_("start of the cycle"))
    cycle_end = models.DateField(verbose_name=_("end of the cycle"))
    frequency = models.PositiveIntegerField(verbose_name=_("frequency"))
    # strict_status = models.BooleanField(verbose_name=_("strict"), max_length=255)
    timesheet = models.ManyToManyField(TimeTable, verbose_name=_('time'))


class Cure(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_("title"), max_length=255)
    dose = models.FloatField(verbose_name=_("dose"), validators=[MinValueValidator(0.0)])
    dose_type = models.CharField(verbose_name=_("dose type"), max_length=255, choices=DOSE_CHOICES)
    schedule = models.ForeignKey(Schedule, verbose_name=_("schedule"), on_delete=models.CASCADE)
    type = models.CharField(verbose_name=_("type"), max_length=255, choices=TYPE_CHOICES)
    strict_status = models.BooleanField(verbose_name=_("strict"), max_length=255, null=True, default=False)
    # просто для справки
    food = models.CharField(verbose_name=_("food"), max_length=255, choices=FOOD_CHOICES, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('id',)


class Photo(models.Model):
    file = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.file.name
