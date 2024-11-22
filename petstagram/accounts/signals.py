import logging

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

from petstagram.accounts.models import Profile
from services.ses import send_email_to_user

logger = logging.getLogger(__name__)

UserModel = get_user_model()


def send_welcome_email_to_user(user):
    subject = "Welcome to Our Platform"
    plain_text = f"Hi {user.email}, welcome to our platform!"
    html_content = f"""
        <html>
            <body>
                <h1>Welcome, {user.email}!</h1>
                <p>We're excited to have you join us.</p>
                <p>Visit us: <a href="https://ourplatform.com">Click here</a></p>
            </body>
        </html>
        """
    try:
        # print(f"Attempting to send email to {user.email}")  # Debugging
        send_email_to_user(user, subject, plain_text=plain_text, html_content=html_content)
        # print(f"Email sent successfully to {user.email}")  # Debugging
    except Exception as e:
        print(f"Failed to send email to {user.email}: {e}")


@receiver(post_save, sender=UserModel)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        try:
            if not hasattr(instance, "profile"):
                Profile.objects.create(user=instance)
        except IntegrityError as e:
            logger.warning(f"Could not create profile for {instance.email}: {e}")

        if not instance.is_staff:
            # print(f"Signal triggered for user: {instance.email}")  # Debugging
            logger.info(f"Sending welcome email to {instance.email} (ID: {instance.id})")
            try:
                send_welcome_email_to_user(instance)
            except Exception as e:
                logger.error(f"Failed to send welcome email to {instance.email}: {e}")
