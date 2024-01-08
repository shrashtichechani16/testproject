import csv
from io import StringIO
from celery import shared_task
from .models import Student, Parent, AcademicDetails
from datetime import datetime
from django.db import transaction


@shared_task
def process_csv_data(csv_data):
    csv_file = StringIO(csv_data)
    reader = csv.DictReader(csv_file)
    required_columns = ['name', 'gender', 'adhar_card_number', 'dob', 'identification_marks', 'category',
                        'height', 'weight', 'mail_id', 'contact_detail', 'address',
                        'father_name', 'father_qualification', 'father_profession', 'father_designation',
                        'father_aadhar_card', 'father_mobile_number', 'father_mail_id',
                        'mother_name', 'mother_qualification', 'mother_profession', 'mother_designation',
                        'mother_aadhar_card', 'mother_mobile_number', 'mother_mail_id',
                        'class_name', 'section', 'date_of_joining', 'session']

    # Check if all required columns are present
    missing_columns = set(required_columns) - set(reader.fieldnames)
    if missing_columns:
        return f"Error: Missing required columns - {', '.join(missing_columns)}."

    for row in reader:
        missing_data_columns = [column for column in required_columns if not row.get(column)]
        if missing_data_columns:
            return f"Error: Missing data in columns - {', '.join(missing_data_columns)}."
        try:
            with transaction.atomic():
                dob = datetime.strptime(row['dob'], '%Y-%m-%d').date()
                date_of_joining = datetime.strptime(row['date_of_joining'], '%Y-%m-%d').date()
                student = Student.objects.create(
                    name=row['name'],
                    gender=row['gender'],
                    adhar_card_number=row['adhar_card_number'],
                    dob=dob,
                    identification_marks=row['identification_marks'],
                    category=row['category'],
                    height=row['height'],
                    weight=row['weight'],
                    mail_id=row['mail_id'],
                    contact_detail=row['contact_detail'],
                    address=row['address'],
                )
                parent = Parent.objects.create(
                    father_name=row['father_name'],
                    father_qualification=row['father_qualification'],
                    father_profession=row['father_profession'],
                    father_designation=row['father_designation'],
                    father_aadhar_card=row['father_aadhar_card'],
                    father_mobile_number=row['father_mobile_number'],
                    father_mail_id=row['father_mail_id'],
                    mother_name=row['mother_name'],
                    mother_qualification=row['mother_qualification'],
                    mother_profession=row['mother_profession'],
                    mother_designation=row['mother_designation'],
                    mother_aadhar_card=row['mother_aadhar_card'],
                    mother_mobile_number=row['mother_mobile_number'],
                    mother_mail_id=row['mother_mail_id'],
                    student=student
                )
                academic_details, created = AcademicDetails.objects.get_or_create(
                    student=student,
                    defaults={
                        'class_name': row['class_name'],
                        'section': row['section'],
                        'date_of_joining': date_of_joining,
                        'session':row['session']
                    }
                )

                if not created:
                    academic_details.class_name = row['class_name']
                    academic_details.section = row['section']
                    academic_details.date_of_joining = date_of_joining
                    academic_details.save()

        except Exception as e:
            return f"Error: {str(e)}"

    return "CSV data processed successfully."