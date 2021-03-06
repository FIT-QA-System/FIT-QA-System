# Generated by Django 2.0.3 on 2018-04-04 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0026_auto_20180403_2121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pastquestion',
            old_name='questions',
            new_name='question',
        ),
        migrations.AddField(
            model_name='pastquestion',
            name='answer',
            field=models.TextField(default="Can't answer", verbose_name='Answer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pastquestion',
            name='category',
            field=models.IntegerField(default=0, verbose_name='Category'),
            preserve_default=False,
        ),
    ]
