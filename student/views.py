from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StudentSerializer,StudentSerializerForGET,CSVFileUploadSerializer
from student.utils import send_admin_notification,send_student_mail
from rest_framework.parsers import FileUploadParser
from student.tasks import process_csv_data
from drf_yasg.utils import swagger_auto_schema


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    @swagger_auto_schema(
        request_body=StudentSerializer,
        responses={
            status.HTTP_201_CREATED: "Student data created successfully",
            status.HTTP_400_BAD_REQUEST: "Invalid input data",
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.perform_create(serializer)
        instance = serializer.instance
        send_student_mail(instance, instance.academic_detail.first())
        send_admin_notification(instance, instance.academic_detail.first())
        return Response("Student data created successfully ", status=status.HTTP_201_CREATED)
    @swagger_auto_schema(
        request_body=StudentSerializer,
        responses={
            status.HTTP_200_OK: "Student data updated successfully",
            status.HTTP_400_BAD_REQUEST: "Invalid input data",
        }
    )
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Student data updated successfully"}, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: "Student data deleted successfully",
            status.HTTP_404_NOT_FOUND: "Student not found",
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Student data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: "Details of a specific student",
            status.HTTP_404_NOT_FOUND: "Student not found",
        }
    )
    def get_serializer_class(self):
            if self.action in ['list', 'retrieve']:
                return StudentSerializerForGET
            return StudentSerializer
   


class CSVFileUploadViewSet(viewsets.ViewSet):
    serializer_class = CSVFileUploadSerializer
    @swagger_auto_schema(
        request_body=CSVFileUploadSerializer,
        responses={
            status.HTTP_202_ACCEPTED: "CSV file is being processed.",
            status.HTTP_400_BAD_REQUEST: "Invalid CSV file",
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            csv_file = request.FILES['csv_file']
            csv_data = csv_file.read().decode('utf-8')
            process_csv_data.delay(csv_data)
            return Response({'message': 'CSV file is being processed.'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

