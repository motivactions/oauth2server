from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from auths.tasks import send_mail as send_mail_task
from auths.helpers import get_site_serializer


class AccountAdapter(DefaultAccountAdapter):

    """Custom Allauth Account Adapter"""

    def send_mail(self, template_prefix, email, context):
        from django.contrib.sites.models import Site

        current_site = context.get("current_site", None)
        if isinstance(current_site, (Site,)):
            current_site = get_site_serializer(current_site)
            context["current_site"] = current_site

        user = context.get("user", None)
        if user is not None:
            user = user.to_dict()
            context["user"] = user

        context["request"] = None
        context["to_email"] = email
        context["subject"] = render_to_string(
            "{0}_subject.txt".format(template_prefix), context
        )
        send_mail_task.delay(template_prefix, context)

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        print(activate_url)
        to_email = emailconfirmation.email_address.email
        user = emailconfirmation.email_address.user
        context = {
            "user": user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
        }
        if signup:
            email_template = "account/email/auth_email_confirmation_signup"
        else:
            email_template = "account/email/auth_email_confirmation"
        self.send_mail(email_template, to_email, context)
