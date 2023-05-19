from rest_framework import serializers

from .models import Cure, Photo, Schedule, TimeTable


class MainTimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = '__all__'


class MainScheduleSerializer(serializers.ModelSerializer):
    timesheet = MainTimeTableSerializer(many=True)

    def create(self, validated_data):
        timesheet_data = validated_data.pop('timesheet')
        s = MainTimeTableSerializer(data=timesheet_data, many=True)
        s.is_valid(raise_exception=True)
        schedule = super().create(validated_data)
        timesheet_models = s.save()
        schedule.timesheet.set(timesheet_models)
        return schedule

    class Meta:
        model = Schedule
        fields = '__all__'


class ViewOnlyScheduleSerializer(serializers.ModelSerializer):
    timesheet = MainTimeTableSerializer(many=True)

    class Meta:
        model = Schedule
        fields = '__all__'


class MainCureSerializer(serializers.ModelSerializer):
    schedule = MainScheduleSerializer()

    def create(self, validated_data):
        schedule_data = validated_data.pop('schedule')
        s = MainScheduleSerializer(data=schedule_data)
        s.is_valid(raise_exception=True)
        schedule_model = s.save()
        validated_data['patient'] = self.context['request'].user.patient
        validated_data['schedule'] = schedule_model
        cure = super().create(validated_data)
        return cure

    def update(self, instance, validated_data):
        schedule_data = validated_data.pop('schedule')
        s = MainScheduleSerializer(data=schedule_data)
        s.is_valid(raise_exception=True)
        schedule_model = s.save()
        validated_data['schedule'] = schedule_model
        cure = super().update(instance, validated_data)
        return cure

    class Meta:
        model = Cure
        fields = (
            'id',
            'title',
            'dose',
            'dose_type',
            'type',
            "schedule",
            "food",
            "strict_status",
        )


class ViewOnlyCureSerializer(serializers.ModelSerializer):
    schedule = ViewOnlyScheduleSerializer()

    class Meta:
        model = Cure
        fields = '__all__'


# ?? IDK for 10 days reports
class CureSerializer(serializers.ModelSerializer):
    def to_representation(self, model):
        return {'cure': MainCureSerializer(model).data, 'timetable': MainTimeTableSerializer(model).data}

    class Meta:
        model = Cure
        fields = "__all__"


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = "__all__"
