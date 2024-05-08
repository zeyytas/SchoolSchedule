from uuid import uuid4

from freezegun import freeze_time
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status

from school.models import Schedule
from school.tests.factories.schedule_factory import ScheduleFactory
from school.tests.factories.school_class_factory import ClassFactory
from school.tests.factories.student_factory import StudentFactory
from school.tests.factories.subject_factory import SubjectFactory
from school.tests.factories.user_factory import UserFactory


class TestScheduleAPI(APITestCase):
    """
    Test case for the Schedule API endpoints.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.student = StudentFactory()
        cls.class_obj = ClassFactory(name="8A")
        cls.class_obj2 = ClassFactory(name="8C")
        cls.subject = SubjectFactory(name="math")
        cls.subject2 = SubjectFactory(name="science")

        schedules_data = [
            {
                "school_class": cls.class_obj,
                "subject": cls.subject,
                "day_of_week": "Tuesday",
                "hour": 9,
            },
            {
                "school_class": cls.class_obj2,
                "subject": cls.subject,
                "day_of_week": "Wednesday",
                "hour": 10,
            },
            {
                "school_class": cls.class_obj,
                "subject": cls.subject,
                "day_of_week": "Thursday",
                "hour": 11,
            },
            {
                "school_class": cls.class_obj,
                "subject": cls.subject2,
                "day_of_week": "Monday",
                "hour": 14,
            },
        ]

        cls.schedule1, cls.schedule2, cls.schedule3, cls.schedule4 = [
            ScheduleFactory(**data) for data in schedules_data
        ]

        cls.path = reverse("schedule-list")

    def setUp(self) -> None:
        self.client.force_authenticate(self.user)

    def _get_with_token(self, token):
        self.client.logout()
        return self.client.get(self.path, **{"HTTP_AUTHORIZATION": f"Bearer {token}"})

    @staticmethod
    def _create_response_dict(schedule):
        """
        Create a response dictionary for a schedule.
        """
        return {
            "class": {
                "name": schedule.school_class.name,
                "student_count": schedule.school_class.students.count(),
            },
            "subject": {"name": schedule.subject.name},
            "teacher": {"name": schedule.subject.teacher.name},
            "day_of_week": schedule.day_of_week,
            "hour": schedule.hour,
        }

    def test_get_schedule_list_with_valid_token(self):
        """Test getting the schedule list with a valid access token."""
        response = self._get_with_token(AccessToken.for_user(self.user))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], Schedule.objects.count())

    def test_get_schedule_list_with_invalid_token(self):
        """Test getting the schedule list with an invalid access token."""
        response = self._get_with_token(uuid4())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @freeze_time("2024-05-07")  # Here the day is Tuesday
    def test_get_class_schedule_for_today(self):
        """Test retrieving schedule for a class for today."""
        response = self.client.get(
            self.path, {"for_today": "true", "class_name": self.class_obj.name}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = self._create_response_dict(self.schedule1)
        self.assertEqual(response.json()["results"][0], expected_data)

    def test_filter_by_day_of_week(self):
        """Test filtering schedules by day of the week."""
        response = self.client.get(self.path, {"day_of_week": "Tuesday"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = self._create_response_dict(self.schedule1)
        self.assertEqual(response.json()["results"][0], expected_data)

    def test_filter_by_class_name(self):
        """Test filtering schedules by class name."""
        response = self.client.get(self.path, {"class_name": self.class_obj.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            self._create_response_dict(self.schedule1),
            self._create_response_dict(self.schedule3),
            self._create_response_dict(self.schedule4),
        ]
        expected_data.sort(key=lambda x: (x["day_of_week"], x["hour"]))
        self.assertListEqual(response.json()["results"], expected_data)

    def test_filter_by_teacher_name(self):
        """Test filtering schedules by teacher name."""
        response = self.client.get(
            self.path, {"teacher_name": self.subject.teacher.name}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            self._create_response_dict(self.schedule1),
            self._create_response_dict(self.schedule2),
            self._create_response_dict(self.schedule3),
        ]
        expected_data.sort(key=lambda x: (x["day_of_week"], x["hour"]))
        self.assertEqual(response.json()["results"], expected_data)

    def test_filter_by_hour(self):
        """Test filtering schedules by hour."""
        response = self.client.get(self.path, {"hour": 9})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = self._create_response_dict(self.schedule1)
        self.assertEqual(response.json()["results"][0], expected_data)

    def test_filter_by_subject_name(self):
        """Test filtering schedules by subject name."""
        response = self.client.get(self.path, {"subject_name": self.subject.name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()["count"],
            Schedule.objects.filter(subject=self.subject).count(),
        )
