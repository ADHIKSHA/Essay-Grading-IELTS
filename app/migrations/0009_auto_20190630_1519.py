# Generated by Django 2.2.2 on 2019-06-30 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20190630_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='givetake',
            name='starttime',
            field=models.IntegerField(),
        ),
    ]
