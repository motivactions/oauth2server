import logging
from time import sleep

from celery import shared_task

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string

from .utils import get_bot_user

logger = logging.getLogger("engine")


def message(msg, level=0):
    print(f"{msg}")


def render_mail(template_prefix, context):
    """
    Renders an e-mail to `email`.  `template_prefix` identifies the
    e-mail that is to be sent, e.g. "account/email/email_confirmation"
    context = {
        "subject": str,
        "message": str,
        "to_email": list or str,
        "from_email": str or None,
    }
    """
    email = context.get("to_email", list())
    to_emails = [email] if isinstance(email, str) else email
    subject = context.get("subject", "Email form %s" % settings.SITE_DOMAIN).strip()

    get_from_email = context.get("from_email", None)
    from_email = get_from_email if get_from_email else settings.DEFAULT_FROM_EMAIL

    bodies = {}
    for ext in ["html", "txt"]:
        try:
            template_name = "{0}_message.{1}".format(template_prefix, ext)
            bodies[ext] = render_to_string(template_name, context).strip()
        except TemplateDoesNotExist:
            if ext == "txt" and not bodies:
                # We need at least one body
                raise
    if "txt" in bodies:
        msg = EmailMultiAlternatives(subject, bodies["txt"], from_email, to_emails)
        if "html" in bodies:
            msg.attach_alternative(bodies["html"], "text/html")
    else:
        msg = EmailMessage(subject, bodies["html"], from_email, to_emails)
        msg.content_subtype = "html"  # Main content is now text/html
    return msg


@shared_task(name="auths.send_mail")
def send_mail(template_prefix, context):
    msg = render_mail(template_prefix, context)
    msg.send()


@shared_task(name="oauth.clear_tokens", bind=True)
def clear_tokens(self):
    from oauth2_provider.models import clear_expired

    clear_expired()
