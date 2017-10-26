from django.db import models

from ...models import CharFieldTranslatable
from ...models import TextFieldTranslatable


class FakeModel(models.Model):
    char_field = CharFieldTranslatable(max_length=8)
    text_field = TextFieldTranslatable()
