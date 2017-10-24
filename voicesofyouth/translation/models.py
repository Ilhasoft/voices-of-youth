from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from psycopg2 import ProgrammingError

from .fields import CharFieldTranslatable
from .fields import TextFieldTranslatable


class TranslatableModel(models.Model):
    model = models.CharField(max_length=128)
    verbose_name = models.CharField(max_length=128)
    verbose_name_plural = models.CharField(max_length=128)

    def __str__(self):
        return self.model


class TranslatableField(models.Model):
    model = models.ForeignKey(TranslatableModel)
    field = models.CharField(max_length=128)
    verbose_name = models.CharField(max_length=128)

    class Meta:
        unique_together = ('model', 'field')

    def __str__(self):
        return f'{self.model}.{self.verbose_name}'


class Translation(models.Model):
    field = models.ForeignKey(TranslatableField)
    language = models.CharField(max_length=2, choices=settings.LANGUAGES)
    translation = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('language', 'field')

    def __str__(self):
        return f'{field}({self.language})'


# Store the fields that need translation.
translatable_fields = []


@receiver(post_migrate)
def create_translations(app_config, **_):
    if settings.PROJECT_NAME in app_config.name:
        for model in app_config.get_models():
            print_title = True
            for field in model._meta.get_fields():
                if type(field) in (CharFieldTranslatable, TextFieldTranslatable):
                    if print_title:
                        print_title = not print_title
                        print("{:=^80}".format(f' Translatable fields '))
                        print("{:-^80}".format(f' {app_config.name}.{model.__name__} '))
                        model_instance = TranslatableModel.objects.get_or_create(model=model._meta.model_name)[0]
                    translatable_fields.append({'model': model_instance,
                                                'field': field.attname,
                                                'verbose_name': field.verbose_name})
                    print(field.verbose_name)
        try:
            TranslatableModel.objects.all()
            while len(translatable_fields) > 0:
                field_data = translatable_fields.pop(0)
                TranslatableField.objects.get_or_create(**field_data)
        except ProgrammingError:
            """
            If this exception occur here, is because the translation app migration has not yet performed.
            """
