# Generated by Django 2.2.2 on 2019-07-05 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_contactdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='CohessionData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_rep', models.CharField(max_length=100)),
                ('s_rep', models.CharField(max_length=100)),
                ('preplex_score', models.CharField(max_length=50)),
                ('relevance', models.CharField(max_length=50)),
                ('para', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'CohessionData',
            },
        ),
    ]
