from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
class Student(models.Model):
    GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('OBC', 'OBC'),
        ('SC', 'SC'),
        ('ST', 'ST'),
    ]

    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    adhar_card_number = models.CharField(max_length=12,unique=True)
    dob = models.DateField()
    identification_marks = models.TextField(null=True,blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    height = models.CharField(max_length=20,null=True,blank=True)
    weight = models.CharField(max_length=20,null=True,blank=True)
    mail_id = models.EmailField(unique=True)
    contact_detail = models.CharField(max_length=15)
    address = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class Parent(models.Model):
    father_name = models.CharField(max_length=255)
    father_qualification = models.CharField(max_length=255)
    father_profession = models.CharField(max_length=255)
    father_designation = models.CharField(max_length=255)
    father_aadhar_card = models.CharField(max_length=20)
    father_mobile_number = models.CharField(max_length=15)
    father_mail_id = models.EmailField(unique=True)

    mother_name = models.CharField(max_length=255)
    mother_qualification = models.CharField(max_length=255)
    mother_profession = models.CharField(max_length=255,null=True,blank=True)
    mother_designation = models.CharField(max_length=255,null=True,blank=True)
    mother_aadhar_card = models.CharField(max_length=20)
    mother_mobile_number = models.CharField(max_length=15)
    mother_mail_id = models.EmailField(unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    student = models.ForeignKey(Student, related_name='parent', on_delete=models.CASCADE,null=True,blank=True)

class AcademicDetails(models.Model):
    student = models.ForeignKey(Student, related_name='academic_detail',on_delete=models.CASCADE,null=True,blank=True)
    enrollment_id = models.CharField(max_length=12, unique=True, blank=True)
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    date_of_joining = models.DateField(null=True,blank=True)
    session=models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.enrollment_id:
            name_prefix = self.student.name[:3].upper()
            random_number = format(get_random_string(length=3, allowed_chars='123456789'), '0<3')
            enrollment_date = timezone.now().strftime('%d%m%y')
            self.enrollment_id = f"{enrollment_date}{name_prefix}{random_number}"
        super().save(*args, **kwargs)



def document_upload_path(instance, filename):
    student_name = instance.student.name if instance.student else 'unknown_student'
    return f"student_documents/{student_name}/{filename}"

class Document(models.Model):
    student = models.ForeignKey(Student, related_name='document', on_delete=models.CASCADE,null=True,blank=True)
    student_documents = models.FileField(upload_to=document_upload_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
