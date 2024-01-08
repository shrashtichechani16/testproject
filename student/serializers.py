from rest_framework import serializers
from .models import Student, Parent, Document, AcademicDetails

class CSVFileUploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()
    def validate_csv_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("File must have a .csv format.")
        return value
        

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'
    

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class AcademicDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicDetails
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    parent = ParentSerializer(required=False)
    document = DocumentSerializer(required=False)
    academic_detail = AcademicDetailsSerializer(required=False)

    class Meta:
        model = Student
        fields = '__all__'
        depth = 1
    def create(self, validated_data):
        parent_data = validated_data.pop('parent')
        academic_data = validated_data.pop('academic_detail')
        document_data = validated_data.pop('document')

        student = Student.objects.create(**validated_data)
        Parent.objects.create(student=student, **parent_data)
        AcademicDetails.objects.update_or_create(student=student, defaults={**academic_data})
        Document.objects.create(student=student, **document_data)

        return student
    
    def update(self, instance, validated_data):
        parent_data = validated_data.pop('parent')
        academic_data = validated_data.pop('academic_detail')
        document_data = validated_data.pop('document')
        for field in self.fields:
            if field in validated_data and validated_data[field] is not None:
                setattr(instance, field, validated_data[field])

        if parent_data:
            parent_instance = instance.parent.first() if instance.parent.exists() else None
            parent_serializer = ParentSerializer(parent_instance, data=parent_data, partial=True)
            if parent_serializer.is_valid(raise_exception=True):
                parent_serializer.save()

        if academic_data:
            academic_instance = instance.academic_detail.first() if instance.academic_detail.exists() else None
            academic_serializer = AcademicDetailsSerializer(academic_instance, data=academic_data, partial=True)
            if academic_serializer.is_valid(raise_exception=True):
                academic_serializer.save()

        if document_data:
            document_instance = instance.document.first() if instance.document.exists() else None
            document_serializer = DocumentSerializer(document_instance, data=document_data, partial=True)
            if document_serializer.is_valid(raise_exception=True):
                document_serializer.save()

        instance.save()
        return instance
    
class StudentSerializerForGET(serializers.ModelSerializer):
    parent = ParentSerializer(many=True, read_only=True)
    document = DocumentSerializer(many=True, read_only=True)
    academic_detail = AcademicDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = '__all__'
