from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


@method_decorator([login_required], name="dispatch")
class AccountIndexView(TemplateView):
    template_name = "account/index.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({"title": _(f"Welcome {self.request.user}")})


@method_decorator([login_required], name="dispatch")
class AccountProfileView(TemplateView):
    template_name = "account/profile.html"
    extra_context = {"title": _("My Profile")}
