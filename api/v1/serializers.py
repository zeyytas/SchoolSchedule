from rest_framework import serializers
from school.models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Schedule model.
    """

    class Meta:
        model = Schedule
        fields = ["day_of_week", "hour"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["class"] = {
            "name": instance.school_class.name,
            "student_count": instance.school_class.students.count(),
        }
        representation["teacher"] = {
            "name": instance.subject.teacher.name,
        }
        representation["subject"] = {
            "name": instance.subject.name,
        }

        return representation
