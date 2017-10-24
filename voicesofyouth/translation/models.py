"""
The VoY project need the data have translation for some records, this app will help us in this task.
"""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from psycopg2 import ProgrammingError

from .fields import CharFieldTranslatable
from .fields import TextFieldTranslatable


__author__ = ['Elton Pereira', ]
__email__ = 'eltonplima AT gmail DOT com'
__status__ = 'Development'


class TranslatableModel(models.Model):
    """
    Stores which model that have fields that can be translated.

    Attributes:
        model: Model name.
        verbose_name: Verbose name from model.
        verbose_name_plural: Plural version of verbose name.
    """
    model = models.CharField(max_length=128)
    verbose_name = models.CharField(max_length=128)
    verbose_name_plural = models.CharField(max_length=128)

    def __str__(self):
        return self.model


class TranslatableField(models.Model):
    """
    Stores which fields that can be translated.

    Attributes:
        model: Model TranslatableModel instance.
        field: Name of the field.
        verbose_name: Verbose name of the field.
    """
    model = models.ForeignKey(TranslatableModel)
    field = models.CharField(max_length=128)
    verbose_name = models.CharField(max_length=128)

    class Meta:
        unique_together = ('model', 'field')

    def __str__(self):
        return f'{self.model}.{self.verbose_name}'


class Translation(models.Model):
    """
    Stores the translation.

    Attributes:
        field: TranslatableField instance.
        language: What is the language of this translation.
        translation: Translation itself.
        content_type: Content type of the original model instance(**you don't need to manipulate this field**).
        object_id: ID of the original model instance(**you don't need to manipulate this field**).
        content_object: Object instance itself.
    """
    field = models.ForeignKey(TranslatableField)
    language = models.CharField(max_length=2, choices=settings.LANGUAGES)
    translation = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('language', 'field', 'content_type', 'object_id')

    def __str__(self):
        return f'{self.field}({self.language})'


# Store the fields that need translation.
translatable_fields = []


@receiver(post_migrate)
def create_translations(app_config, **_):
    """
    Populates the translation app models with all models that use the fields CharFieldTranslatable or
    TextFieldTranslatable.

    .. note::
        This function is called when migrate runs.
    """
    if settings.PROJECT_NAME in app_config.name:
        for model in app_config.get_models():
            print_title = True
            for field in model._meta.get_fields():
                if type(field) in (CharFieldTranslatable, TextFieldTranslatable):
                    if print_title:
                        print_title = not print_title
                        print("{:=^80}".format(f' Translatable fields '))
                        print("{:-^80}".format(f' {app_config.name}.{model.__name__} '))
                        data = {'model': model._meta.model_name,
                                'verbose_name': model._meta.verbose_name,
                                'verbose_name_plural': model._meta.verbose_name_plural}
                        model_instance = TranslatableModel.objects.update_or_create(**data, defaults=data)[0]
                    translatable_fields.append({'model': model_instance,
                                                'field': field.attname,
                                                'verbose_name': field.verbose_name})
                    print(field.verbose_name)
        try:
            TranslatableModel.objects.all()
            while len(translatable_fields) > 0:
                field_data = translatable_fields.pop(0)
                TranslatableField.objects.update_or_create(model=field_data['model'],
                                                           field=field_data['field'],
                                                           defaults=field_data)
        except ProgrammingError:
            """
            If this exception occur here, is because the translation app migration has not yet performed.
            """
