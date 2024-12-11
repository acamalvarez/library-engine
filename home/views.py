import logging

import requests
from django.conf import settings
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        api_url = "https://api.api-ninjas.com/v1/quote"
        headers = {"X-Api-Key": settings.API_KEY}
        response = requests.get(api_url, headers=headers)

        if response.status_code == requests.codes.ok:
            context["quote"] = response.json()[0]["quote"]
            context["author"] = response.json()[0]["author"]
        else:
            logger.error(response.text)

        return context
