from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # If the social account is already linked, do nothing
        if sociallogin.is_existing:
            return

        # Try to find a user with the same email address
        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                # Connect this social account with the existing user
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                # No user with this email exists, Allauth will create a new one
                pass

       