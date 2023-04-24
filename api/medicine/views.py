import datetime
import json
from django.contrib.auth.models import User

# import matplotlib.pyplot as plt
# import numpy as np
from django.shortcuts import get_object_or_404
from managment.models import Patient, Guardian
from django.utils import timezone
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from statistic.models import TakenMed, MissedMed
from statistic.serializers import TakenMedSerializer,MissedMedSerializer
from managment.utils import get_type_of_user

from .models import Cure, TimeTable, Schedule
from .serializers import (
    CureSerializer,
    MainScheduleSerializer,
    MainCureSerializer,
    MainTimeTableSerializer,
    ViewOnlyCureSerializer,
)
from rest_framework.exceptions import ValidationError


class CollectStatisticView(generics.ListAPIView):
    """отчет за последни е 10 дней"""

    permission_classes = (IsAuthenticated,)
    queryset = Cure.objects.all()
    serializer_class = CureSerializer

    def list(self, request, *args, **kwargs):
        cures = Cure.objects.filter(user=request.user.patient)
        cures_taken = TakenMed.objects.filter(user=request.user.patient)
        cures_taken = [c.id for c in cures_taken]
        today = datetime.datetime.now().astimezone(timezone.get_current_timezone()).date()
        missed_count = 0
        taken_count = 0

        for cure in cures:
            if cure.schedule.cycle_start <= today and cure.schedule.cycle_end >= today:
                tmp = {}
                tmp["cure"] = MainCureSerializer(cure).data
                if cure.id not in cures_taken:
                    missed_count += 0
                    MissedMed.objects.create(patient=request.user.patient, med=cure, date=today, is_informed=False)

                else:
                    taken_count += 1
        # TODO:
        data = {}
        with open('data.json') as json_file:
            data = json.load(json_file)
            data["data"]["taken"].append(taken_count)
            data["data"]["missed"].append(missed_count)

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
        x, y = None, None

        with open('data.json') as json_file:
            # raise Exception(json.load(json_file))
            data = json.load(json_file)
            x = data["data"]["taken"]
            y = data["data"]["missed"]
        # if len(x) > 10:
        #     x, y = x[-10:], y[-10:]
        # barWidth = 0.3
        # r1 = np.arange(len(x))
        # r2 = [x + barWidth for x in r1]
        # plt.bar(r1, x, width=barWidth, color='blue', edgecolor='black', capsize=7, label='3')
        #
        # plt.bar(r2, y, width=barWidth, color='orange', edgecolor='black', capsize=7, label='4')
        # titles = ["taken", "missed"]
        #
        # plt.xticks([r + barWidth for r in range(len(x))], titles, rotation=90, fontsize=5)
        # plt.ylabel('height')
        # plt.subplots_adjust(bottom=0.5, top=0.99)
        # plt.legend()
        # plt.savefig('graf.png')

        return Response({}, status=status.HTTP_200_OK)


class TakeViewSet(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        queryset = Cure.objects.filter(patient__user=request.user)
        cure = get_object_or_404(queryset, pk=pk)
        today = datetime.datetime.now().astimezone(timezone.get_current_timezone()).date()
        today_time = datetime.datetime.now().astimezone(timezone.get_current_timezone())
        flag_is_late = True
        if cure.schedule.cycle_start <= today and cure.schedule.cycle_end >= today:
            tmp = {}
            tmp["cure"] = MainCureSerializer(cure).data
            times = MainTimeTableSerializer(TimeTable.objects.filter(schedule=cure.schedule), many=True).data

            for t in times:
                time_processed = datetime.datetime.strptime(t["time"], '%H:%M:%S')
                if not cure.strict_status:

                    if time_processed.hour == today_time.hour:

                        flag_is_late = False
                        # raise Exception(time_processed.hour ,today_time.hour)
                        break
                    else:

                        flag_is_late = True
                        break

                else:
                    if time_processed.hour == today_time.hour and time_processed.minute == today_time.minute:
                        flag_is_late = False
                        # raise Exception(time_processed.hour ,today_time.hour)
                        break
                    else:
                        flag_is_late = True
                        break
            if not flag_is_late:
                taken_med = TakenMed.objects.create(
                    patient=request.user.patient, med=cure, date=today_time, report=False, is_late=flag_is_late
                )
                serializer = TakenMedSerializer(taken_med)
            else:
                missed_med = MissedMed.objects.create(
                    patient=request.user.patient, med=cure, date=today_time, is_informed=False
                )
                serializer = MissedMedSerializer(missed_med)
        else:
            return Response({"error": "no need to take it"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)


class CureViewSet(viewsets.ModelViewSet):
    serializer_class = MainCureSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        if request.GET.get("ward") is not None:
            try:
                id = int(request.GET.get("ward"))
                ward = Patient.objects.get(id=id)
                request.user = ward.user
            except Exception:
                raise ValidationError({"detail": "404 bad ward"})
        return super().create(request)

    def update(self, request, *args, **kwargs):
        if request.GET.get("ward") is not None:
            try:
                id = int(request.GET.get("ward"))
                ward = Patient.objects.get(id=id)
                request.user = ward.user
            except Exception:
                raise ValidationError({"detail": "404 bad ward"})
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

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

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ViewOnlyCureSerializer
        else:
            return MainCureSerializer

    def get_queryset(self):
        type_user = get_type_of_user(self.request.user)
        if type_user == "guardian":
            try:
                ward = int(self.request.query_params['ward'])
                ward = Patient.objects.get(id=ward)

            except Exception:
                raise ValidationError({"detail": "404 bad ward"})
            return Cure.objects.filter(patient=ward)
        else:
            return Cure.objects.filter(patient__user=self.request.user)


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = MainScheduleSerializer
    permission_classes = (IsAuthenticated,)


class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = MainTimeTableSerializer
    permission_classes = (IsAuthenticated,)
