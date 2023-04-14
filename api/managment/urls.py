from django.urls import path
from rest_framework import routers

from .views import (
    DoctorViewSet,
    DoctorVisitViewSet,
    GuardianViewSet,
    PatientSettingViewSet,
    PatientViewSet,
    TariffViewSet,
    TranzactionViewSet,
    WhoIAmView,
    change_password_view,
)

router = routers.DefaultRouter()
router.register('patients', PatientViewSet, basename='patients')
router.register('settings', PatientSettingViewSet, basename='settings')
router.register('guardians', GuardianViewSet, basename='guardians')
router.register('tariff', TariffViewSet, basename='tariff')
router.register('tranzaction', TranzactionViewSet, basename='tranzaction')
router.register('doctor', DoctorViewSet, basename='doctor')
router.register('doctorvisit', DoctorVisitViewSet, basename='doctorvisit')

urlpatterns = [
    path('whoiam/', WhoIAmView.as_view()),
    path('change-password/', change_password_view),
]
urlpatterns += router.urls
