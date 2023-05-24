from django.urls import include, path, re_path
from rest_framework import routers

from .views import CollectStatisticView, CureViewSet, PhotoViewSet, ScheduleViewSet, TakeViewSet, TimeTableViewSet,CureViewDateSet

router = routers.DefaultRouter()
router.register('cure', CureViewSet, basename='cure')
router.register('cure_date', CureViewDateSet, basename='cure')
router.register('schedule', ScheduleViewSet, basename='schedule')
router.register('time', TimeTableViewSet, basename='time')
router.register('photos', PhotoViewSet, basename='photos')

data_pattern = "(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"

urlpatterns = [
    path('stat/', CollectStatisticView.as_view()),
    path('take/cure/<int:pk>/', TakeViewSet.as_view()),
]
urlpatterns += router.urls
