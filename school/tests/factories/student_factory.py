import factory

from school.models import Student
from school.tests.factories.school_class_factory import ClassFactory


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    name = factory.Faker("name")
    school_class = factory.SubFactory(ClassFactory)
