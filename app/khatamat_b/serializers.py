from rest_framework.exceptions import ValidationError
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from dj_rest_auth.registration.serializers import RegisterSerializer
from api.models import MyUser

class CustomRegisterSerializer(RegisterSerializer):
    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if email:
            existing_user = MyUser.objects.filter(email=email).first()
            if existing_user:
                # Check if the email is verified
                email = EmailAddress.objects.filter(email=email).first()
                if email:
                    if email.verified:
                        raise ValidationError(
                            "A user is already registered with this e-mail address.",
                            code='email_verified_conflict'
                        )
                    else:
                        # Handle unverified email case
                        raise ValidationError(
                            "This email is already registered but not verified. Please check your email for verification instructions.",
                            code='email_unverified_conflict'
                        )
        return email

