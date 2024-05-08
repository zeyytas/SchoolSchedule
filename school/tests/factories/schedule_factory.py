import factory

from school.models import Schedule
from school.tests.factories.school_class_factory import ClassFactory
from school.tests.factories.subject_factory import SubjectFactory


class ScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Schedule

    day_of_week = factory.Faker(
        "random_element",
        elements=[
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
    )
    hour = factory.Faker("random_int", min=8, max=15)
    school_class = factory.SubFactory(ClassFactory)
    subject = factory.SubFactory(SubjectFactory)
