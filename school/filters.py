from django.utils import timezone
from django_filters import rest_framework as filters
from .models import Schedule


class CustomScheduleFilter(filters.FilterSet):
    """
    Custom filter set for filtering Schedule objects.
    """

    for_today = filters.BooleanFilter(method="filter_for_today")
    class_name = filters.CharFilter(field_name="school_class__name")
    teacher_name = filters.CharFilter(field_name="subject__teacher__name")
    subject_name = filters.CharFilter(field_name="subject__name")

    def filter_for_today(self, queryset, name, value):
        if value:
            today = timezone.now().date()
            return queryset.filter(day_of_week=today.strftime("%A"))
        return queryset

    class Meta:
        model = Schedule
        fields = [
            "for_today",
            "class_name",
            "day_of_week",
            "hour",
            "teacher_name",
            "subject_name",
        ]
