import factory

from school.models import Subject
from school.tests.factories.teacher_factory import TeacherFactory


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject

    name = factory.Faker("word")
    teacher = factory.SubFactory(TeacherFactory)
