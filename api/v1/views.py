from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from api.v1.serializers import ScheduleSerializer
from school.filters import CustomScheduleFilter
from school.models import Schedule


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling Schedule instances.
    """

    queryset = Schedule.objects.select_related(
        "school_class", "subject", "subject__teacher"
    ).order_by("day_of_week", "hour")
    serializer_class = ScheduleSerializer
    filterset_class = CustomScheduleFilter
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    # TODO: I would dive into concurrency optimizations for handling more than 5000 RPS
    # TODO: Some other pagination could be a better choice, e.g. CursorPagination

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        """
        Override the default list method to cache the response for 60 seconds.
        """
        return super().list(request, *args, **kwargs)
