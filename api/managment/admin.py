from django.contrib import admin

from .models import (
    Buyer,
    Doctor,
    DoctorVisit,
    Guardian,
    GuardianSetting,
    Patient,
    PatientGuardianRelation,
    PatientSetting,
    Tariff,
    Tranzaction,
)


# Register your models here.
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass


@admin.register(PatientSetting)
class PatientSettingAdmin(admin.ModelAdmin):
    pass


@admin.register(GuardianSetting)
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


@admin.register(PatientGuardianRelation)
class PatienGuardianRelationAdmin(admin.ModelAdmin):
    pass


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    pass
