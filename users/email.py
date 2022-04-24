from djoser import email
from djoser import utils
from djoser.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings as django_settings
from django.contrib.sites.models import Site

class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'users/reset_password_email_form.html'

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()
        current_site = Site.objects.get_current().domain
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        context["domain"] = current_site

        return context


class ActivationEmail(email.ActivationEmail):
    template_name = "users/activation_email_form.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()
        current_site = Site.objects.get_current().domain
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        context["domain"] = current_site
        return context
