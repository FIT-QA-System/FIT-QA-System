# Generated by Django 2.0.2 on 2018-03-17 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0016_auto_20180317_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='parent_department_id',
            field=models.CharField(max_length=20, null=True, verbose_name='Parent Department ID'),
        ),
    ]
