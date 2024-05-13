# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Department, Batch, University, Section, Subject
import datetime
from django.db import IntegrityError, transaction

@receiver(post_save, sender=Department)
def Create_Batches(sender, instance, created, **kwargs):
    if created and University.objects.filter(pk=instance.university.pk).exists():
        semester_type = University.objects.get(pk=instance.university.pk).semester_type
        sections = instance.sections
        print(sections)
        for i in range(4):
            if semester_type == 'Fall':
                Batch.objects.create(semester_code=(i*2)+1, department=instance, year=(datetime.date.today().year)-i,batch_sections=sections[3-i])
            elif semester_type == 'Spring':
                Batch.objects.create(semester_code=(i*2)+2, department=instance, year=(datetime.date.today().year)-1-i,batch_sections=sections[3-i])

@receiver(post_save, sender=Batch)
def Create_Sections(sender, instance, created, **kwargs):
    if created:
        department = Department.objects.get(pk=instance.department.pk)
        sections = instance.batch_sections
        for i in range(instance.batch_sections):
            section_name = f"B{department.department_code}-{instance.semester_code}{chr(65+i)}"
            Section.objects.create(section_name=section_name,batch=instance)
            
# @receiver(post_save, sender=Section)
# def Create_Subjects(sender, instance, created, **kwargs):
#     if created:
#         subject_name = [f"{instance.section_name}-{i}" for i in range(5)]
#         try:
#             with transaction.atomic():
#                 Subject.objects.create(batch_id=instance.batch.pk,subjects_1=subject_name,)
#         except IntegrityError:
#             pass