# Generated by Django 2.0.2 on 2018-03-17 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0015_auto_20180317_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='contact_website',
            field=models.URLField(null=True, verbose_name='Website'),
        ),
    ]
