from rest_framework import authentication

from voicesofyouth.user.models import User


class GuestAuthentication(authentication.BaseAuthentication):
    """
    This class return the 'correct' anonymous user.

    In some circumstances, user can create data without authentication. E.g. Comments in reports.
    """
    def authenticate(self, request):
        user = User.objects.get(username='guest')
        return user, None
