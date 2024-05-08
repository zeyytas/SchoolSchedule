import random
import string

import factory

from school.models import Class


class ClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Class

    name = f"{random.randint(1, 10)}{random.choice(string.ascii_letters)}"
