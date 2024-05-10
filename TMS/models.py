from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    verification_code = models.IntegerField(blank=True,null=True)
    verified = models.BooleanField(default=False,blank=True,null=True)
    approved = models.BooleanField(default=False,blank=True,null=True)

class University(models.Model):
    university_name = models.CharField(max_length=50)
    university_location = models.CharField(max_length=50)
    university_email = models.CharField(max_length=15)
    CHOICES = [
        ('Fall','Fall'),
        ('Spring','Spring'),
    ]
    semester_type = models.CharField(max_length=6, choices=CHOICES)

    def __str__(self):
        return f"{self.university_name}, {self.university_location}, {self.semester_type}"

class Department(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="university_department")
    department_name = models.CharField(max_length=30)
    department_code = models.CharField(max_length=3)
    sections = ArrayField(models.IntegerField())

    def __str__(self):
        return f"{self.department_name}: {self.department_code}"

class Batch(models.Model):
    semester_code = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="batch_dept")
    year = models.IntegerField()
    batch_sections = models.IntegerField()

    def __str__(self):
        return f"Batch: {self.year}, {self.department.department_code}, {self.semester_code}th Semester"
    
class Section(models.Model):
    section_name = models.CharField(max_length=6)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="section_batch")

    def __str__(self):
        return f"{self.section_name}"

class Subject(models.Model):
    batch = models.OneToOneField(Batch, on_delete=models.CASCADE, related_name="batch_subjects")
    # subjects_3 = ArrayField(
    #     models.CharField(max_length=20, blank=True)
    # )
    subjects_1 = ArrayField(
        models.CharField(max_length=20, blank=True)
    )
    
    def __str__(self):
        return f"{self.batch}"

class Teacher(models.Model):
    teacher_name = models.CharField(max_length=30)
    subjects = models.ManyToManyField(Subject, related_name="teacher_subjects")

    def __str__(self):
        return f"{self.teacher_name}"

class Venue(models.Model):
    venue_code = models.CharField(max_length=10)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.venue_code}: {self.capacity}"

class Timing(models.Model):
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.day_of_week}: {self.start_time} to {self.end_time}"

class Timetable_components(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="component_section")
    subject = models.CharField(max_length=20, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="component_teacher")

    def __str__(self):
        return f"{self.subject}, {self.section}, {self.teacher}"
    