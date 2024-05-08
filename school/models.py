from django.db import models


class Class(models.Model):
    """Model representing a class."""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    """Model representing a student."""

    name = models.CharField(max_length=50)
    school_class = models.ForeignKey(
        "Class", on_delete=models.CASCADE, related_name="students"
    )

    def __str__(self):
        return self.name


class Subject(models.Model):
    """Model representing a subject."""

    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(
        "Teacher", on_delete=models.CASCADE, related_name="subjects_taught"
    )

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """Model representing a teacher."""

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    """Model representing a schedule."""

    DAY_CHOICES = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]

    HOUR_CHOICES = [
        (8, "8 AM"),
        (9, "9 AM"),
        (10, "10 AM"),
        (11, "11 AM"),
        (12, "12 PM"),
        (13, "1 PM"),
        (14, "2 PM"),
        (15, "3 PM"),
    ]

    day_of_week = models.CharField(max_length=20, choices=DAY_CHOICES)
    hour = models.IntegerField(choices=HOUR_CHOICES)
    school_class = models.ForeignKey(
        "Class", on_delete=models.CASCADE, related_name="schedules"
    )
    subject = models.ForeignKey(
        "Subject", on_delete=models.CASCADE, related_name="schedules", db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["school_class", "day_of_week", "hour"], name="unique_schedule"
            )
        ]

    def __str__(self):
        return f"Schedule for {self.day_of_week} at {self.hour}"
