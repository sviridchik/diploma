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
    change_password_view,
    GuardianSettingViewSet,
    ConnectionViewSet,
    BuyViewSet,
    CodeGenerateViewSet,
    VisitViewDateSet
)
from rest_framework import routers


router = routers.DefaultRouter()
router.register('patients', PatientViewSet, basename='patients')
router.register('settings_guard', GuardianSettingViewSet, basename='settings_guard')
router.register('settings', PatientSettingViewSet, basename='settings')
router.register('guardians', GuardianViewSet, basename='guardians')
router.register('tariff', TariffViewSet, basename='tariff')
router.register('tranzaction', TranzactionViewSet, basename='tranzaction')
router.register('doctor', DoctorViewSet, basename='doctor')
router.register('doctorvisit', DoctorVisitViewSet, basename='doctorvisit')
router.register('doctorvisit_date', VisitViewDateSet, basename='doctorvisit')
router.register('connect', ConnectionViewSet, basename='connect')
router.register('code', CodeGenerateViewSet, basename='code')


urlpatterns = [
    path('whoiam/', WhoIAmView.as_view()),
    path('change-password/', change_password_view),
    path("buy/", BuyViewSet.as_view({'post': 'create'})),
]
urlpatterns += router.urls
