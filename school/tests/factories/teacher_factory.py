import factory

from school.models import Teacher


class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teacher

    name = factory.Faker("name")
