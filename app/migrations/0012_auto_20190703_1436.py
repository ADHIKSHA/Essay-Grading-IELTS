# Generated by Django 2.2.2 on 2019-07-03 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_scoredata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scoredata',
            old_name='userid',
            new_name='Email',
        ),
        migrations.RenameField(
            model_name='scoredata',
            old_name='grade',
            new_name='Trained_Data_result',
        ),
        migrations.RenameField(
            model_name='scoredata',
            old_name='wordcount',
            new_name='Word_Count',
        ),
    ]
