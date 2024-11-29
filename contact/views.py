import logging
from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.views.generic import FormView

from .forms import ContactForm

logger = logging.getLogger(__name__)


class ContactView(FormView):
    form_class = ContactForm
    template_name = "contact/contact_form.html"
    success_url = "/contact/"

    def form_valid(self, form: Any) -> HttpResponse:
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]
        name = form.cleaned_data["name"]

        email_message = f"From: {email}\n{name}\n{message}"

        try:
            send_mail(
                subject=form.cleaned_data["subject"],
                message=email_message,
                from_email="",
                recipient_list=[settings.EMAIL_HOST_USER],
            )
            logger.info("Email send correctly")
        except:
            logger.error("The was an error with sending email.")

        try:
            form.save()
        except:
            logger.error("There was an error saving the form.")

        return super().form_valid(form)