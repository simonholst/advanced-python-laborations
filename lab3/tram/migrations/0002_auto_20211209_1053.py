# Generated by Django 3.2.10 on 2021-12-09 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tram', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dep', models.CharField(max_length=200)),
                ('dest', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Fruit',
        ),
    ]
