# Generated by Django 3.2.8 on 2022-01-23 15:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20220108_1550'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='completetask',
            options={'ordering': ['-upload_date']},
        ),
        migrations.AlterField(
            model_name='completetask',
            name='upload_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='projectorder',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='projectorder',
            name='number_of_pages',
            field=models.IntegerField(help_text='0 words approx'),
        ),
    ]