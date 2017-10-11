from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gismodels
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from sorl.thumbnail.fields import ImageField


class VoyUser(AbstractUser):
    display_name = models.CharField(max_length=32, null=True, blank=True)
    language = models.CharField(max_length=90, choices=settings.LANGUAGES, default='en')
    user_image = ImageField(verbose_name=_('Image'), upload_to='user/profile', null=True, blank=True)
    personal_url = models.URLField(null=True, blank=True)
    hometown = models.CharField(max_length=128, null=True, blank=True)
    can_post_to_social_networks = models.BooleanField(default=False)
    location = gismodels.PointField(null=True, blank=True, srid=4326)


# We put this code here to centralize all references to User model.
User = get_user_model()
