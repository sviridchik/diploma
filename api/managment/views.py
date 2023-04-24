from django.contrib.auth.models import User
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .utils import get_type_of_user
from .models import Patient, PatientSetting, Guardian, Tariff, Tranzaction, Doctor, DoctorVisit,GuardianSetting
from .serializers import (
    PatientSerializer,
    PatientSettingSerializer,
    GuardianSerializer,
    TariffSerializer,
    TranzactionSerializer,
    DoctorVisitSerializer,
    DoctorSerializer,
    UserSerializer,
    ReadOnlyDoctorVisitSerializer,
    ChangePasswordSerializer,
    DoctorVisitViewOnlySerializer,
GuardianSettingSerializer
)
from rest_framework.permissions import IsAuthenticated
from .models import PatienGuardianRelation
from rest_framework.exceptions import ValidationError


class WhoIAmView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        user = request.user
        patient = Patient.objects.filter(user=user)
        guardian = Guardian.objects.filter(user=user)
        res = {"type": None, "user": None}
        if len(patient) != 0:
            res["type"] = "patient"
            res["user"] = PatientSerializer(tuple(patient)[0]).data
        elif len(guardian) != 0:
            res["type"] = "guardian"
            res["user"] = GuardianSerializer(tuple(guardian)[0]).data
        else:
            res["type"] = "nothing"
            res["user"] = UserSerializer(user).data

        return Response(res, status=status.HTTP_200_OK)


class WardViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.get(user=self.request.user)

    def get_queryset(self):
        guardian = Guardian.objects.get(user=self.request.user)
        ward_list = PatienGuardianRelation.objects.filter(guardian=guardian)
        ward_list = [ward.patient for ward in ward_list]
        return ward_list


class PatientViewSet(viewsets.mixins.CreateModelMixin, viewsets.mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.get(user=self.request.user)

    def get_queryset(self):
        user: User = self.request.user
        if user.is_superuser:
            return Patient.objects.all()
        else:
            return Patient.objects.filter(user=user)


class PatientSettingViewSet(viewsets.ModelViewSet):
    queryset = PatientSetting.objects.all()
    serializer_class = PatientSettingSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.get(patient=self.request.user.patient)

    def get_queryset(self):
        user: User = self.request.user
        if user.is_superuser:
            return PatientSetting.objects.all()
        else:
            return PatientSetting.objects.filter(patient=user.patient)

class GuardianSettingViewSet(viewsets.ModelViewSet):
    queryset = GuardianSetting.objects.all()
    serializer_class = GuardianSettingSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.get(guardian=self.request.user.guardian)

    def get_queryset(self):
        user: User = self.request.user
        if user.is_superuser:
            return GuardianSetting.objects.all()
        else:
            return GuardianSetting.objects.filter(guardian=user.guardian)

class GuardianViewSet(viewsets.mixins.CreateModelMixin, viewsets.mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = GuardianSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.get(user=self.request.user)

    def get_queryset(self):
        user: User = self.request.user
        if user.is_superuser:
            return Guardian.objects.all()
        else:
            return Guardian.objects.filter(user=user)


class TariffViewSet(viewsets.ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer
    permission_classes = [IsAuthenticated]


class TranzactionViewSet(viewsets.ModelViewSet):
    queryset = Tranzaction.objects.all()
    serializer_class = TranzactionSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        if request.GET.get("ward") is not None:
            try:
                id = int(self.request.query_params['ward'])
                ward = Patient.objects.get(id=id)
                request.user = ward.user
            except Exception:
                raise ValidationError({"detail":"404 bad ward"})
        return super().create(request)

    def get_queryset(self):
        type_user = get_type_of_user(self.request.user)
        if type_user == "guardian":
            try:
                ward = int(self.request.query_params['ward'])
                ward = Patient.objects.get(id=ward)
            except Exception:
                raise ValidationError({"detail":"404 bad ward"})
            return Doctor.objects.filter(patient=ward)
        else:
            return Doctor.objects.filter(patient__user=self.request.user)


class DoctorVisitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return DoctorVisitViewOnlySerializer
        else:
            return DoctorVisitSerializer

# raise ValidationError({"detail": "404 bad ward"})

    def create(self, request):
        if request.GET.get("ward") is not None:
            try:
                id = int(request.GET.get("ward"))
                ward = Patient.objects.get(id=id)
                request.user = ward.user
            except Exception:
                raise ValidationError({"detail": "404 bad ward"})
        # do your thing here
        return super().create(request)

    def destroy(self, request, *args, **kwargs):
        if request.GET.get("ward") is not None:
            try:
                id = int(request.GET.get("ward"))
                ward = Patient.objects.get(id=id)
                request.user = ward.user
            except Exception:
                raise ValidationError({"detail": "404 bad ward"})

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        type_user = get_type_of_user(self.request.user)
        if type_user == "guardian":
            try:
                ward = int(self.request.query_params['ward'])
                ward = Patient.objects.get(id=ward)
            except Exception:
                raise ValidationError({"detail": "404 bad ward"})
            return DoctorVisit.objects.filter(patient=ward)
        else:
            return DoctorVisit.objects.filter(patient__user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadOnlyDoctorVisitSerializer
        else:
            return DoctorVisitSerializer


@api_view(http_method_names=['PATCH'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    serializer = ChangePasswordSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
