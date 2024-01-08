from django.core.mail import send_mail
from harbie import settings

def send_student_mail(student, academic_details):
    subject = f"Welcome to Dummy School, {student.name}!"
    message = f"Dear {student.name},\nYou are enrolled in Dummy School. Your Enrollment ID is {academic_details.enrollment_id}. Provide us with the required documents for future references.\n\nTeam Dummy School"
    sender = settings.EMAIL_HOST_USER
    send_mail(subject, message, sender, [student.mail_id])


def send_admin_notification(student, academic_details):
    subject = f"New Enrollment at Dummy School"
    message = f"Dear Admin,\nNew student {student.name} enrolled in class {academic_details.class_name}, section {academic_details.section} with enrollment ID {academic_details.enrollment_id} in {academic_details.session} session."
    sender = settings.EMAIL_HOST_USER
    admin_email = 'durganand.jha@habrie.com'
    send_mail(subject, message, sender, [admin_email])
