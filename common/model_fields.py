from django.db import models


class CharFieldWithoutChoicesMigrations(models.CharField):
    """Overwrites models.CharField in order to avoid migration creation every time we change `choices` value.

    TODO consider to replace in Django 5.0 `Changed in Django 5.0: Support for mappings and callables was added.`
         https://docs.djangoproject.com/en/5.1/ref/models/fields/#choices
    """

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Remove `choices` from kwargs so Django doesn't detect it as a change
        kwargs.pop("choices", None)
        return name, path, args, kwargs
