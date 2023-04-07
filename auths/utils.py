import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.utils import timezone


logger = logging.getLogger("django")


def get_users_online(request):
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get("_auth_user_id", None))
    # Query all logged in users based on id list
    return get_user_model().objects.filter(id__in=uid_list)


def get_bot_user():
    User = get_user_model()
    bot_username = getattr(settings, "BOT_USERNAME", None)
    if bot_username:
        bot = User.objects.get(username=bot_username)
    else:
        bot = User.objects.filter(is_superuser=True).first()
    return bot
