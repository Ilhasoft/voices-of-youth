import json

from django import forms
from django.contrib.contenttypes.models import ContentType

from .models import Translation
from .models import TranslatableModel
from .models import TranslatableField

class TranslationsField(forms.CharField):
    model = None
    model_ct = None

    def __init__(self, model, *args, **kwargs):
        super(TranslationsField, self).__init__(*args, **kwargs)
        self.model = model
        self.model_ct = ContentType.objects.get_for_model(self.model)

    def clean(self, *args, **kwargs):
        full_value = super(TranslationsField, self).clean(*args, **kwargs)

        translations = json.loads(full_value)
        value = []

        for language, data in translations.items():
            fields = data.get('fields')
            for field_data in fields:
                name = field_data.get('name')[len('translate-'):]
                translation = field_data.get('value')

                translatable_model = TranslatableModel.objects.get(model=self.model._meta.model_name)
                field = TranslatableField.objects.get(
                    model=translatable_model,
                    field_name=name,
                )

                value.append(Translation(
                    field=field,
                    language=language,
                    translation=translation,
                    content_type=self.model_ct,
                ))
        return value
