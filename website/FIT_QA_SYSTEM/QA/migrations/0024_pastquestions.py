# Generated by Django 2.0.3 on 2018-04-04 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0023_word_standard'),
    ]

    operations = [
        migrations.CreateModel(
            name='PastQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', models.ManyToManyField(related_name='_pastquestions_questions_+', to='QA.PastQuestions')),
            ],
        ),
    ]
