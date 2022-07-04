from django.db import models


class Handbook(models.Model):
    """Модель сущность Справочник
    """
    handbook_id = models.PositiveIntegerField(
        'handbook id',
        help_text='Идентификатор справочника',
    )

    title = models.CharField(
        'title',
        max_length=250,
        help_text='Наименование',
    )

    short_title = models.CharField(
        'short title',
        max_length=50,
        help_text='Короткое наименование',
    )

    description = models.TextField(
        'description',
        max_length=500,
        help_text='Описание',
    )

    version = models.CharField(
        'version',
        max_length=20,
        help_text='Версия',
    )

    start_at = models.DateField(
        'start at',
        help_text='Дата начала действия справочника этой версии',
    )

    def __str__(self) -> str:
        return '{} - {} ({})'.format(
            self.handbook_id, self.short_title, self.version
        )


class HandbookElement(models.Model):
    """Модель сущности Элемент справочника
    """

    handbook_id = models.ForeignKey(
        Handbook,
        on_delete=models.CASCADE,
        related_name='elements',
        help_text='Родительский идентификатор',
    )

    element_code = models.CharField(
        'element code',
        max_length=20,
        help_text='Код элемента',
    )

    value = models.CharField(
        'element value',
        max_length=50,
        help_text='Значение элемента',
    )

    def __str__(self) -> str:
        return '{} ({})'.format(
            self.element_code, self.handbook_id
        )
