# Generated by Django 2.0.2 on 2018-03-17 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0012_auto_20180317_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='supervisee',
            field=models.CharField(max_length=100, null=True, verbose_name='Supervisee'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='supervisor',
            field=models.CharField(max_length=100, null=True, verbose_name='Supervisor'),
        ),
    ]
