from choices import COLORS_CHOICES, LANGUAGE_CHOICES, SPEC_CHOICES
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    age = models.PositiveIntegerField(verbose_name=_('age'), validators=[MaxValueValidator(150)])
    phone = models.BigIntegerField(verbose_name=_('phone'), default=0, blank=True, unique=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Guardian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    phone = models.BigIntegerField(verbose_name=_('phone'), default=0, blank=True, unique=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
class GuardianSetting(models.Model):
    guardian = models.OneToOneField(Guardian, on_delete=models.CASCADE)
    language = models.CharField(verbose_name=_("language"), max_length=255, choices=LANGUAGE_CHOICES)
    theme = models.CharField(verbose_name=_("color"), max_length=255, choices=COLORS_CHOICES, default="white")



class PatientGuardianRelation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    banned = models.BooleanField(
        _('banned'), help_text="Был ли он забанен опекуном через администратора", default=False
    )
    should_send_report = models.BooleanField(
        _('should send report'), help_text="Отправлять ли отчеты об опекуемом", default=True
    )
    relationship = models.CharField(
        _('relationship'), max_length=150, blank=True, help_text="Родство опекуна с опекуемым"
    )

    def __str__(self) -> str:
        return f'{self.guardian} -> {self.patient}'


class PatientSetting(models.Model):
    patient = models.OneToOneField(Patient, verbose_name=_('patient'), on_delete=models.CASCADE)
    color = models.CharField(verbose_name=_("color"), max_length=255, choices=COLORS_CHOICES, default="white")
    font = models.IntegerField(verbose_name=_('font'))
    city = models.CharField(verbose_name=_("city"), max_length=255)
    language = models.CharField(verbose_name=_("language"), max_length=255, choices=LANGUAGE_CHOICES)


class Tariff(models.Model):
    price = models.DecimalField(verbose_name=_("price"), max_digits=20, decimal_places=12)
    date = models.DateTimeField(verbose_name=_("date_start"))
    duration_days = models.PositiveIntegerField(verbose_name=_("duration_days"))
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)


class Tranzaction(models.Model):
    bill = models.CharField(verbose_name=_("bill"), max_length=255)
    date = models.DateTimeField(verbose_name=_("date_start"))
    method = models.CharField(verbose_name=_("billing method"), max_length=255)
    user = models.ForeignKey(Patient, on_delete=models.CASCADE)


class Doctor(models.Model):
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    specialty = models.CharField(_('specialty'), max_length=150, blank=True, choices=SPEC_CHOICES)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


class DoctorVisit(models.Model):
    date = models.DateTimeField(verbose_name=_("date_start"))
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


@receiver(post_save,sender=Patient)
def add_basic_setting(sender,instance,created,**kwargs):
    if created:
        PatientSetting.objects.create(patient = instance,color="white",font=14,city="Minsk",language="RUSSIAN")

@receiver(post_save,sender=Guardian)
def add_basic_setting(sender,instance,created,**kwargs):
    if created:
        GuardianSetting.objects.create(guardian = instance,language="RUSSIAN",theme="white")

