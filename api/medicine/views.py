import datetime
import json

import pytesseract
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q

# import matplotlib.pyplot as plt
# import numpy as np
from django.shortcuts import get_object_or_404
from django.utils import timezone
from managment.models import Guardian, GuardianSetting, Patient
from managment.utils import get_type_of_user
from PIL import Image
from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from statistic.models import MissedMed, TakenMed
from statistic.serializers import MissedMedSerializer, TakenMedSerializer
from thefuzz import fuzz, process

from .models import Cure, Photo, Schedule, TimeTable
from .serializers import (
    CureSerializer,
    MainCureSerializer,
    MainScheduleSerializer,
    MainTimeTableSerializer,
    PhotoSerializer,
    ViewOnlyCureSerializer,
)


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

class CureViewDateSet(viewsets.ModelViewSet):
    serializer_class = MainCureSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        date_send = request.GET.get('date', '')
        if len(date_send)>0:
            date_send = date_send.split("-")
            date_send = [el.strip("'") for el in date_send]
            date_send = [el.strip('"') for el in date_send]
            date_send = datetime.date(int(date_send[0]),int(date_send[1]),int(date_send[2]))

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(Q(schedule__cycle_start__lte=date_send) & Q(schedule__cycle_end__gte=date_send)
                                   | Q(schedule__cycle_start=date_send)| Q(schedule__cycle_end=date_send) )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        type_user = get_type_of_user(self.request.user)
        if type_user == "guardian":
            try:
                guardian = Guardian.objects.get(user=self.request.user)
                ward = GuardianSetting.objects.get(guardian=guardian).patient_current
            except Exception:
                raise ValidationError({"detail": "404 bad ward"})
            return Cure.objects.filter(patient=ward)
        else:
            return Cure.objects.filter(patient__user=self.request.user)
class CureViewSet(viewsets.ModelViewSet):
    serializer_class = MainCureSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        type_user = get_type_of_user(self.request.user)
        if type_user == "guardian":
            try:
                guardian = Guardian.objects.get(user=self.request.user)
                ward = GuardianSetting.objects.get(guardian=guardian).patient_current
                request.user = ward.user
            except Exception:
                raise ValidationError({"detail": "404 bad ward"})
        return super().create(request)

    def get_queryset(self):
        type_user = get_type_of_user(self.request.user)
        if type_user == "guardian":
            try:
                guardian = Guardian.objects.get(user=self.request.user)
                ward = GuardianSetting.objects.get(guardian=guardian).patient_current
            except Exception:
                raise ValidationError({"detail": "404 bad ward"})
            return Cure.objects.filter(patient=ward)
        else:
            return Cure.objects.filter(patient__user=self.request.user)

    def update(self, request, *args, **kwargs):
        type_user = get_type_of_user(self.request.user)
        if type_user == "guardian":
            try:
                guardian = Guardian.objects.get(user=self.request.user)
                ward = GuardianSetting.objects.get(guardian=guardian).patient_current
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
        type_user = get_type_of_user(self.request.user)
        if type_user == "guardian":
            try:
                guardian = Guardian.objects.get(user=self.request.user)
                ward = GuardianSetting.objects.get(guardian=guardian).patient_current
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


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = MainScheduleSerializer
    permission_classes = (IsAuthenticated,)


class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = MainTimeTableSerializer
    permission_classes = (IsAuthenticated,)


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        type_user = get_type_of_user(self.request.user)
        if type_user == "patient":
            patient = self.request.user.patient
            chosen_lang = patient.patientsetting.language
            tess_lang = {'RUSSIAN': 'rus', 'ENGLISH': 'eng'}[chosen_lang]
            img1 = Image.open(request.data['file'])
            text = pytesseract.image_to_string(img1, config=settings.TESSERACT_CONFIG + f' -l {tess_lang}')
            print(text)
            cures_titles = patient.cure_set.all().values_list('title', flat=True)
            matches = process.extract(text, cures_titles, scorer=fuzz.partial_ratio, limit=10)
            cure_id_by_title = dict(patient.cure_set.values_list('title', 'id'))
            matches_with_cure_id = [
                {'title': match[0], 'id': cure_id_by_title[match[0]], 'score': match[1]} for match in matches
            ]
            return Response(matches_with_cure_id)
        else:
            raise ValidationError({"detail": "You are not patient"})
