# Generated by Django 3.2.13 on 2022-07-04 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Handbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handbook_id', models.PositiveIntegerField(help_text='Идентификатор справочника', verbose_name='handbook id')),
                ('title', models.CharField(help_text='Наименование', max_length=250, verbose_name='title')),
                ('short_title', models.CharField(help_text='Короткое наименование', max_length=50, verbose_name='short title')),
                ('description', models.TextField(help_text='Описание', max_length=500, verbose_name='description')),
                ('version', models.CharField(help_text='Версия', max_length=20, verbose_name='version')),
                ('start_at', models.DateField(help_text='Дата начала действия справочника этой версии', verbose_name='start at')),
            ],
        ),
        migrations.CreateModel(
            name='HandbookElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element_code', models.CharField(help_text='Код элемента', max_length=20, verbose_name='element code')),
                ('value', models.CharField(help_text='Значение элемента', max_length=50, verbose_name='element value')),
                ('handbook_id', models.ForeignKey(help_text='Родительский идентификатор', on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='handbooks.handbook')),
            ],
        ),
    ]