import datetime
import json
from managment.models import Guardian
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.response import Response
from managment.utils import get_type_of_user
from managment.models import Patient, Guardian
from rest_framework.exceptions import ValidationError

# import numpy as np
from .models import Devise, Logs, MissedMed, TakenMed, Achievement, Label
from .serializers import (
    DeviseSerializer,
    LogsSerializer,
    MissedMedSerializer,
    TakenMedSerializer,
    AchievementSerializer,
    LabelSerializer,
)

# import matplotlib.pyplot as plt


class AnalyticTakenGuardianView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = TakenMed.objects.all()
    serializer_class = TakenMedSerializer

    def get_queryset(self):
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        # TODO:to make it right
        user = request.user
        # user = User.objects.filter(username="ivan")[0]
        final_data = {"принятые": 0, "пропущенные": 0}
        if len(Guardian.objects.filter(user=user)) == 0:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        guard = Guardian.objects.filter(user=user)[0]
        if guard.care_about is None:
            return Response({"error": "no patient"}, status=status.HTTP_400_BAD_REQUEST)
        # raise Exception(guard.care_about,guard.care_about is None)
        patient_care_about = guard.care_about
        cures = TakenMed.objects.filter(patient=patient_care_about)
        cures_missed = MissedMed.objects.filter(patient=patient_care_about)
        date_data = request.GET.get("date_data")
        if date_data:
            date_data = date_data.split(".")
            for i in range(len(date_data)):
                if date_data[i].startswith("0"):
                    date_data[i] = date_data[i][1:]
            # raise Exception(date_data)
            date_data = [eval(el) for el in date_data]
            date_data = datetime.date(date_data[-1], date_data[-2], date_data[-3])
            cures = cures.filter(date__date=date_data)
            cures_missed = cures_missed.filter(date__date=date_data)
            res = TakenMedSerializer(cures, many=True)
            res_missed = MissedMedSerializer(cures_missed, many=True)
        else:
            date_data = timezone.now()
            cures = cures.filter(date__date=date_data)
            cures_missed = cures_missed.filter(date__date=date_data)
            res = TakenMedSerializer(cures, many=True)
            res_missed = MissedMedSerializer(cures_missed, many=True)
        final_data["принятые"] = res.data
        final_data["пропущенные"] = res_missed.data
        final_data["подопечный"] = patient_care_about.id
        x, y = None, None
        id_target = patient_care_about.id
        with open('data.json') as json_file:
            # raise Exception(json.load(json_file))
            data = json.load(json_file)["data"]
            # print(data)
            for d in data:
                if d["id"] == id_target:
                    x = d["taken"]
                    y = d["missed"]

                    # print(x, y)
        if len(x) > 10:
            x, y = x[-10:], y[-10:]
        final_data["x"] = x
        final_data["y"] = y

        # barWidth = 0.3
        # r1 = np.arange(len(x))
        # r2 = [x + barWidth for x in r1]
        # # raise Exception(x, y)
        # plt.bar(r1, x, width=barWidth, color='blue', edgecolor='black', capsize=7, label='3')
        # # raise Exception(r1)
        # plt.bar(r2, y, width=barWidth, color='orange', edgecolor='black', capsize=7, label='4')
        # titles = ["taken", "missed"]
        # raise Exception(r1,r2)
        # plt.xticks([r + barWidth for r in range(len(x))], titles, rotation=90, fontsize=5)
        # plt.ylabel('height')
        # plt.subplots_adjust(bottom=0.5, top=0.99)
        # plt.legend()
        # plt.savefig('graf.png')
        return Response(final_data, status=status.HTTP_200_OK)


class AnalyticTakenView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    #
    def list(self, request, *args, **kwargs):
        final_data = {"taken": 0, "missed": 0}

        cures = TakenMed.objects.filter(patient__user=request.user)
        cures_missed = MissedMed.objects.filter(patient__user=request.user)
        date_data = request.query_params.get("date_data")
        if date_data:
            date_data = datetime.datetime.fromisoformat(date_data)
            cures = cures.filter(date__date=date_data)
            cures_missed = cures_missed.filter(date__date=date_data)

        res = TakenMedSerializer(cures, many=True)
        res_missed = MissedMedSerializer(cures_missed, many=True)

        final_data["taken"] = res.data
        final_data["missed"] = res_missed.data
        return Response(final_data, status=status.HTTP_200_OK)


class ReportTakenGuardianView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        final_data = {"taken": 0, "missed": 0}
        if 'as_patient' not in self.request.query_params:
            try:
                ward = int(self.request.query_params['ward'])
                patient = Patient.objects.get(id=ward)
            except Exception:
                raise ValidationError({"detail": _("ward not found")})
        else:
            patient = Patient.objects.get(user=self.request.user)

        #     ==================
        cures = TakenMed.objects.filter(patient=patient)
        cures_missed = MissedMed.objects.filter(patient=patient)
        date_data = request.query_params.get("date_data")
        if date_data:
            date_data = datetime.datetime.fromisoformat(date_data)
            cures = cures.filter(date__date=date_data)
            cures_missed = cures_missed.filter(date__date=date_data)

        res = TakenMedSerializer(cures, many=True)
        res_missed = MissedMedSerializer(cures_missed, many=True)

        final_data["taken"] = res.data
        final_data["missed"] = res_missed.data
        return Response(final_data, status=status.HTTP_200_OK)


class DeviseViewSet(viewsets.ModelViewSet):
    queryset = Devise.objects.all()
    serializer_class = DeviseSerializer
    permission_classes = (IsAuthenticated,)


class LogsViewSet(viewsets.ModelViewSet):
    queryset = Logs.objects.all()
    serializer_class = LogsSerializer
    permission_classes = (IsAuthenticated,)


class LabelViewSet(viewsets.ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = (IsAuthenticated,)


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = (IsAuthenticated,)


class MissedMedViewSet(viewsets.ModelViewSet):
    queryset = MissedMed.objects.all()
    serializer_class = MissedMedSerializer
    permission_classes = (IsAuthenticated,)


class TakenMedViewSet(viewsets.ModelViewSet):
    queryset = TakenMed.objects.all()
    serializer_class = TakenMedSerializer
    permission_classes = (IsAuthenticated,)
