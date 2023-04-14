from django.contrib import admin

from .models import Doctor, DoctorVisit, Guardian, Patient, PatientSetting, Tariff, Tranzaction


# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass


@admin.register(PatientSetting)
class PatientSettingAdmin(admin.ModelAdmin):
    pass


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    pass


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    pass


@admin.register(Tranzaction)
class TranzactionAdmin(admin.ModelAdmin):
    pass


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass


@admin.register(DoctorVisit)
class DoctorVisitAdmin(admin.ModelAdmin):
    pass
