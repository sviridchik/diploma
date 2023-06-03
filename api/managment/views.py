from time import sleep
import datetime
from django.db.models import Q

from django.contrib.auth.models import User
from django.views import View
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
from .serializers import (
    ChangePasswordSerializer,
    DoctorSerializer,
    DoctorVisitSerializer,
    DoctorVisitViewOnlySerializer,
    GuardianSerializer,
    GuardianSettingSerializer,
    PatientGuardianRelationSerializer,
    PatientSerializer,
    PatientSettingSerializer,
    ReadOnlyDoctorVisitSerializer,
    TariffSerializer,
    TranzactionSerializer,
    UserSerializer,
)
from .utils import get_type_of_user, token_to_code


class WhoIAmView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        user = request.user
        patients = Patient.objects.filter(user=user)
        guardians = Guardian.objects.filter(user=user)
        res = dict()
        if patients.exists():
            res["patient"] = PatientSerializer(patients.first()).data

        if guardians.exists():
            guardian = guardians.first()
            res["guardian"] = GuardianSerializer(guardian).data
            connected_patients = Patient.objects.filter(
                id__in=PatientGuardianRelation.objects.filter(guardian=guardian).values('patient')
            )
            res["guardian"]['connected_patients'] = PatientSerializer(connected_patients, many=True).data
            patient_relation_map = dict(
                PatientGuardianRelation.objects.filter(guardian=guardian).values_list('patient_id', 'relationship')
            )
            for patient_data in res["guardian"]['connected_patients']:
                patient_data['relationship'] = patient_relation_map[patient_data['id']]

        res["user"] = UserSerializer(user).data

        res["bought"] = True

        if len(Buyer.objects.filter(user=user)) != 0:
            res["bought"] = True
        else:
            res["bought"] = False

        return Response(res, status=status.HTTP_200_OK)


class WardViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    #
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.get(user=self.request.user)

    def get_queryset(self):
        try:
            guardian = Guardian.objects.get(user=self.request.user)
            ward_list = PatienGuardianRelation.objects.filter(guardian=guardian)
        except User.DoesNotExist:
            raise ValidationError({"detail": "user doesn't exist"})
        except Guardian.DoesNotExist:
            raise ValidationError({"detail": "guardian doesn't exist"})
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
        try:
            if user.is_superuser:
                return PatientSetting.objects.all()
            else:
                return PatientSetting.objects.filter(patient=user.patient)
        except Patient.DoesNotExist:
            raise ValidationError({"detail": "patient doesn't exist"})


class GuardianSettingViewSet(viewsets.ModelViewSet):
    queryset = GuardianSetting.objects.all()
    serializer_class = GuardianSettingSerializer
 
    permission_classes = [IsAuthenticated]
    def get_object(self):
        queryset = GuardianSetting.objects.all()
        # raise  Exception(queryset, GuardianSetting.objects.all())
        return queryset.get(guardian=self.request.user.guardian)

    def get_queryset(self):
        user: User = self.request.user
        try:
            if user.is_superuser:
                return GuardianSetting.objects.all()
            else:
                return GuardianSetting.objects.filter(guardian=user.guardian)
        except Guardian.DoesNotExist:
            raise ValidationError({"detail": "guardian doesn't exist"})


class GuardianViewSet(viewsets.mixins.CreateModelMixin, viewsets.mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = GuardianSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.get(user=self.request.user)

    def get_queryset(self):
        user: User = self.request.user
        try:
            if user.is_superuser:
                return Guardian.objects.all()
            else:
                return Guardian.objects.filter(user=user)
        except User.DoesNotExist:
            raise ValidationError({"detail": "user doesn't exist"})



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
        if 'as_patient' not in self.request.query_params:
            try:
                guardian = Guardian.objects.get(user=self.request.user)
                ward = GuardianSetting.objects.get(guardian=guardian).patient_current
                request.user = ward.user
            except Exception:
                raise ValidationError({"detail": "404 bad ward"})
        return super().create(request)

    def get_queryset(self):
        if 'as_patient' not in self.request.query_params:
            try:
                guardian = Guardian.objects.get(user=self.request.user)
                ward = GuardianSetting.objects.get(guardian=guardian).patient_current
            except Exception:
                raise ValidationError({"detail": "404 bad ward"})
            return Doctor.objects.filter(patient=ward).order_by('id')
        else:
            return Doctor.objects.filter(patient__user=self.request.user).order_by('id')


class DoctorVisitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]


    def create(self, request):
        if 'as_patient' not in self.request.query_params:
            try:
                guardian = Guardian.objects.get(user=self.request.user)
                ward = GuardianSetting.objects.get(guardian=guardian).patient_current
                request.user = ward.user
            except Exception:
                raise ValidationError({"detail": "404 bad ward"})
        return super().create(request)

    def get_queryset(self):
        if 'as_patient' not in self.request.query_params:
            try:
                guardian = Guardian.objects.get(user=self.request.user)
                ward = GuardianSetting.objects.get(guardian=guardian).patient_current
            except Exception:
                raise ValidationError({"detail": "404 bad ward"})
            return DoctorVisit.objects.filter(patient=ward).order_by('id')
        else:
            return DoctorVisit.objects.filter(patient__user=self.request.user).order_by('id')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadOnlyDoctorVisitSerializer
        else:
            return DoctorVisitSerializer

class VisitViewDateSet(viewsets.ModelViewSet):
    # serializer_class = MainCureSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        date_send = request.GET.get('date', '')
        date_send = datetime.datetime.fromisoformat(date_send).date()
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(date__date=date_send)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        if 'as_patient' not in self.request.query_params:
            try:
                guardian = Guardian.objects.get(user=self.request.user)
                ward = GuardianSetting.objects.get(guardian=guardian).patient_current
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


# От тебя создать эндпоинт, который будет принимать 6-ти значный код, should_send_report и relationship.


class ConnectionViewSet(viewsets.ModelViewSet):
    serializer_class = PatientGuardianRelationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        code = request.data['code']
        patient_id = request.data['patient_id']
        patient = Patient.objects.get(id=patient_id)
        token = Token.objects.get(user=patient.user)
        code_valid = token_to_code(str(token))
        if code != code_valid:
            return Response({'detail': "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)
        guardian = Guardian.objects.get(user=request.user)
        should_send_report = request.data['should_send_report']
        relationship = request.data['relationship']
        count_patient_relations_of_guardians = len(PatientGuardianRelation.objects.filter(guardian=guardian))
        count_guardians_of_patient_relations = len(PatientGuardianRelation.objects.filter(patient=patient))
        if (
            count_guardians_of_patient_relations < 3
            and count_patient_relations_of_guardians < 3
            and len(PatientGuardianRelation.objects.filter(patient=patient, guardian=guardian)) == 0
        ):
            PatientGuardianRelation.objects.create(
                patient=patient, guardian=guardian, should_send_report=should_send_report, relationship=relationship
            )
        else:
            return Response({'detail': "Too much connections"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_201_CREATED)


class BuyViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        token = request.data['token']
        sleep(2)
        _, created = Buyer.objects.get_or_create(user=user, token=token)
        if created:
            return Response({}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": 'Already bought'}, status=status.HTTP_400_BAD_REQUEST)


class CodeGenerateViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        code = token_to_code(str(token))
        try:
            return Response({"code": code, 'id': request.user.patient.id})
        except Patient.DoesNotExist:
            raise ValidationError({'detail': 'You are not patient'})
