from django.urls import path
from .views import (
    PatientViewSet,
    PatientSettingViewSet,
    GuardianViewSet,
    TariffViewSet,
    TranzactionViewSet,
    DoctorViewSet,
    DoctorVisitViewSet,
    WhoIAmView,
    DoctorForWardViewSet,
    change_password_view,
)
from rest_framework import routers


router = routers.DefaultRouter()
router.register('patients', PatientViewSet, basename='patients')
router.register('settings', PatientSettingViewSet, basename='settings')
router.register('guardians', GuardianViewSet, basename='guardians')
router.register('tariff', TariffViewSet, basename='tariff')
router.register('tranzaction', TranzactionViewSet, basename='tranzaction')
router.register('doctor', DoctorViewSet, basename='doctor')
router.register('doctorvisit', DoctorVisitViewSet, basename='doctorvisit')
router.register('warddoctor', DoctorForWardViewSet, basename='warddoctor')


urlpatterns = [
    path('whoiam/', WhoIAmView.as_view()),
    path('change-password/', change_password_view),
]
urlpatterns += router.urls
