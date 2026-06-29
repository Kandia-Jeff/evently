from django.core.mail import send_mail
from django.conf import settings


def send_verification_approved_email(user):
    send_mail(
        subject='Your Evently Organiser Account Has Been Verified',
        message=f'Hi {user.username},\n\nYour organiser account has been approved. You can now create and publish events on Evently.\n\nThe Evently Team',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_verification_rejected_email(user):
    send_mail(
        subject='Evently Organiser Verification Update',
        message=f'Hi {user.username},\n\nUnfortunately your verification document was not approved. Please log in and resubmit with a valid official document.\n\nThe Evently Team',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_event_approved_email(event):
    send_mail(
        subject=f'Your Event "{event.title}" Has Been Approved',
        message=f'Hi {event.organiser.username},\n\nYour event "{event.title}" has been approved and is now live on Evently.\n\nThe Evently Team',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[event.organiser.email],
        fail_silently=False,
    )


def send_event_rejected_email(event):
    send_mail(
        subject=f'Your Event "{event.title}" Was Not Approved',
        message=f'Hi {event.organiser.username},\n\nYour event "{event.title}" was not approved. Please log in to review the admin notes and resubmit.\n\nThe Evently Team',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[event.organiser.email],
        fail_silently=False,
    )


def send_flag_notification_email(flag):
    from accounts.models import User
    admins = User.objects.filter(is_staff=True)
    admin_emails = [admin.email for admin in admins]
    if admin_emails:
        send_mail(
            subject=f'New Flag Submitted on Evently',
            message=f'A flag has been submitted on the event "{flag.event.title}" by {flag.user.username}.\n\nReason: {flag.reason}\n\nPlease review it at /flagging/admin/flags/\n\nThe Evently System',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admin_emails,
            fail_silently=False,
        )