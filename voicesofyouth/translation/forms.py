import json

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.conf import settings as django_settings

from .models import Translation
from .models import TranslatableModel
from .models import TranslatableField

class TranslationsField(forms.CharField):
    model = None
    model_ct = None
    _prefix = None

    def __init__(self, model, *args, prefix='translate', **kwargs):
        super(TranslationsField, self).__init__(*args, **kwargs)
        self.model = model
        self.model_ct = ContentType.objects.get_for_model(self.model)
        self._prefix = prefix

    @property
    def prefix(self):
        return '{}-'.format(self._prefix) if self._prefix else ''

    def clean(self, *args, **kwargs):
        full_value = super(TranslationsField, self).clean(*args, **kwargs)

        translations = json.loads(full_value)
        value = []

        for language, data in translations.items():
            fields = data.get('fields')
            for field_data in fields:
                name = field_data.get('name')[len(self.prefix):]
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

    def prepare_value(self, value):
        r = {}
        for language, in value.values_list('language').distinct():
            r[language] = {
                'label': dict(django_settings.LANGUAGES).get(language, language),
                'fields': [{
                    'name': '{}{}'.format(self.prefix, translation_item.field.field_name),
                    'value': translation_item.translation
                } for translation_item in value.filter(language=language)]
            }
        return json.dumps(r)
