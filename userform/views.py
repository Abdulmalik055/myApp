from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from validate_email import validate_email
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        
        if not validate_email(email):
            raise ValidationError("Invalid email address")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        user_data = serializer.data
        subject = 'Form Submission Confirmation'
        message = f'''
        Hi {user_data['full_name']},

        Thank you for filling out the form. Your submission has been successfully received.

        Best regards,
        theChapter
        '''
        html_content = f'''
        <p>Hi {user_data['full_name']},</p>
        <p>Thank you for filling out the form. Your submission has been successfully received.</p>
        <p>Best regards,<br>theChapter</p>
        '''

        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user_data['email']],
                fail_silently=False,
                auth_user=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
                html_message=html_content
            )

        except Exception as e:
            print(e)
            return Response({'detail': 'Error sending email: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
