from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from  .utils import get_type_of_user
from .models import Patient, PatientSetting, Guardian, Tariff, Tokens, Tranzaction, Doctor, DoctorVisit
from .serializers import PatientSerializer, PatientSettingSerializer, GuardianSerializer, TariffSerializer, \
    TokensSerializer, TranzactionSerializer, DoctorVisitSerializer, DoctorSerializer, UserSerializer, ReadOnlyDoctorVisitSerializer
from rest_framework.permissions import IsAuthenticated


class WhoIAmView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        # user = User.objects.all()[0]
        user = request.user
        patient = Patient.objects.filter(user=user)
        guardian = Guardian.objects.filter(user=user)
        res = {"type": None,
               "user": None}
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


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        # raise Exception(request.user, type(request.user))
        user: User = request.user
        return resp


class PatientSettingViewSet(viewsets.ModelViewSet):
    queryset = PatientSetting.objects.all()
    serializer_class = PatientSettingSerializer
    permission_classes = [IsAuthenticated]


class GuardianViewSet(viewsets.ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        # raise Exception(request.user, type(request.user))
        user: User = request.user
        return resp


class TariffViewSet(viewsets.ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer
    permission_classes = [IsAuthenticated]


class TokensViewSet(viewsets.ModelViewSet):
    queryset = Tokens.objects.all()
    serializer_class = TokensSerializer


class TranzactionViewSet(viewsets.ModelViewSet):
    queryset = Tranzaction.objects.all()
    serializer_class = TranzactionSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        type_user = get_type_of_user(self.request.user)
        if type_user == "guardian":
            try:
                ward = int(self.request.GET.get('ward'))
            except Exception:
                raise Exception("404 bad ward")
            return Doctor.objects.filter(patient__user=ward)
        else:
            return Doctor.objects.filter(patient__user=self.request.user)

class DoctorForWardViewSet(viewsets.ModelViewSet):
    """ доктора подопечного (надо еще при выборе проверить что он вообще его подопечный)"""
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Doctor.objects.filter(patient__user=self.request.ward)


class DoctorVisitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DoctorVisit.objects.filter(patient__user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadOnlyDoctorVisitSerializer
        else:
            return DoctorVisitSerializer
