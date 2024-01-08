from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, AcademicDetails

@receiver(post_save, sender=Student)
def create_academic_details(sender, instance, created, **kwargs):
    if created and not AcademicDetails.objects.filter(student=instance).exists():
        AcademicDetails.objects.create(student=instance)

