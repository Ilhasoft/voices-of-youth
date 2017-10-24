from django.contrib import admin

from voicesofyouth.translation.models import TranslatableModel
from voicesofyouth.translation.models import TranslatableField
from voicesofyouth.translation.models import Translation

admin.site.register(TranslatableModel)
admin.site.register(TranslatableField)
admin.site.register(Translation)
