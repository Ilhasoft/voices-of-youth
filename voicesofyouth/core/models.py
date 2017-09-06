from django.db import models

from smartmin.models import SmartModel


class BaseManager(models.Manager):
    def get_queryset(self):
        qs = super(BaseManager, self).get_queryset()
        return qs.filter(is_active=True)


class BaseModel(SmartModel):
    objects = BaseManager()
    default_objects = models.Manager()

    class Meta:
        abstract = True
        default_manager_name = 'default_objects'

    def delete(self, **kwargs):
        self.is_active = False
        self.save()
