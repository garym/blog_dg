from django.conf import settings


def app_title_context_processor(request):
    return {'app_title': settings.APP_TITLE}
