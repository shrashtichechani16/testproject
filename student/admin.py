
from django.contrib import admin
from .models import Parent, Student, AcademicDetails, Document

class ParentAdmin(admin.ModelAdmin):
    list_display = ('student','father_name', 'mother_name', 'father_mail_id', 'mother_mail_id', 'created_at', 'updated_at')
    search_fields = ('student__name','father_name', 'mother_name', 'father_mail_id', 'mother_mail_id')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'adhar_card_number', 'dob', 'mail_id', 'created_at', 'updated_at')
    search_fields = ('name', 'adhar_card_number', 'mail_id')

class AcademicDetailsAdmin(admin.ModelAdmin):
    list_display = ('student', 'enrollment_id', 'class_name', 'section', 'date_of_joining')
    search_fields = ('enrollment_id', 'student__name', 'class_name', 'section')

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('student', 'created_at', 'updated_at')
    search_fields = ('student__name', 'file')


admin.site.register(Parent,ParentAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(AcademicDetails,AcademicDetailsAdmin)
admin.site.register(Document,DocumentAdmin)

