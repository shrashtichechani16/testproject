import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "harbie.settings")
import django

django.setup()

import json
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
import pytest
from student.models import Student
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def valid_student_payload():
    document_file = SimpleUploadedFile("example_document.pdf", b"file_content")

    return {
        "name": "John Doe",
        "gender": "Male",
        "adhar_card_number": "123954189010",
        "dob": "2000-01-01",
        "identification_marks": "Scar on left hand",
        "category": "General",
        "height": 175,
        "weight": 70,
        "mail_id": "poiuy@example.com",
        "contact_detail": "1234567890",
        "address": "123 Main St",
        "parent.father_name": "Father Doe",
        "parent.father_qualification": "Graduate",
        "parent.father_profession": "Engineer",
        "parent.father_designation": "Senior Engineer",
        "parent.father_aadhar_card": "987654321012",
        "parent.father_mobile_number": "9876543210",
        "parent.father_mail_id": "lkjh@example.com",
        "parent.mother_name": "Mother Doe",
        "parent.mother_qualification": "Graduate",
        "parent.mother_profession": "Teacher",
        "parent.mother_designation": "Math Teacher",
        "parent.mother_aadhar_card": "876563210980",
        "parent.mother_mobile_number": "8765432109",
        "parent.mother_mail_id": "mnbv@example.com",
        "academic_detail.class_name": "10th",
        "academic_detail.section": "A",
        "academic_detail.date_of_joining": "2023-01-01",
        "academic_detail.session": "2023-2024",
        "document.student_documents": document_file,
    }

@pytest.fixture
def invalid_student_payload():
    # This payload is intentionally missing required fields
    return {
        "name": "John Doe",
        "gender": "Male",
        "dob": "2000-01-01",
        "identification_marks": "Scar on left hand",
        "category": "General",
    }

@pytest.mark.django_db
def test_create_valid_student(valid_student_payload):
    client = APIClient()
    url = reverse("student-list")
    response = client.post(url, valid_student_payload, format="multipart") 
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_student_with_invalid_data(invalid_student_payload):
    client = APIClient()
    url = reverse("student-list")
    response = client.post(url, json.dumps(invalid_student_payload), content_type="application/json") 
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.fixture
def existing_student():
    # Assuming you have an existing student in the database
    student = Student.objects.create(name="John Doe", gender="Male", adhar_card_number="1234567890", dob="2000-01-01")
    return student

@pytest.fixture
def valid_partial_update_payload(existing_student):
    document_file = SimpleUploadedFile("example_document.pdf", b"file_content")

    return {
        "name": "Updated Name",
        "gender": "Female",
        "adhar_card_number": "9876543210",
        "dob": "1995-05-15",
        "parent.father_name": "Father Doe",
        "parent.father_qualification": "Graduate",
        "parent.father_profession": "Engineer",
        "parent.mother_profession": "Teacher",
        "parent.mother_designation": "Math Teacher",
        "academic_detail.class_name": "10th",
        "academic_detail.section": "A",
        "document.student_documents": document_file,  
    }

@pytest.mark.django_db
def test_partial_update_existing_student(existing_student, valid_partial_update_payload):
    client = APIClient()
    url = reverse("student-detail", args=[existing_student.id])
    response = client.patch(url, valid_partial_update_payload, format="multipart")   
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_destroy_existing_student(existing_student):
    client = APIClient()
    url = reverse("student-detail", args=[existing_student.id])
    response = client.delete(url)   
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.fixture
def existing_student():
    student = Student.objects.create(name="John Doe", gender="Male", adhar_card_number="1234567890", dob="2000-01-01")
    return student

@pytest.mark.django_db
def test_retrieve_student(existing_student):
    client = APIClient()
    url = reverse("student-detail", args=[existing_student.id])
    response = client.get(url)    
    assert response.status_code == status.HTTP_200_OK




from unittest.mock import patch

@pytest.fixture
def valid_csv_file():
    # Create a valid CSV file for testing
    csv_content = "header1,header2\nvalue1,value2"
    return SimpleUploadedFile("test.csv", csv_content.encode("utf-8"))

@pytest.fixture
def invalid_csv_file():
    # Create an invalid file (non-CSV) for testing
    txt_content = "some text content"
    return SimpleUploadedFile("test.txt", txt_content.encode("utf-8"))

@pytest.mark.django_db
def test_upload_valid_csv_file(valid_csv_file):
    client = APIClient()
    url = reverse("csv_file_upload-list")  # Use the basename for reversing the URL

    with patch('student.tasks.process_csv_data.delay') as mock_process_csv_data:
        response = client.post(url, {'csv_file': valid_csv_file}, format='multipart')
    assert response.status_code == status.HTTP_202_ACCEPTED

@pytest.mark.django_db
def test_upload_invalid_csv_file(invalid_csv_file):
    client = APIClient()
    url = reverse("csv_file_upload-list")  # Use the basename for reversing the URL
    response = client.post(url, {'csv_file': invalid_csv_file}, format='multipart')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
 