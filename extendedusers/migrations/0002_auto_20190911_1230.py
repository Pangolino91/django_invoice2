# Generated by Django 2.2.4 on 2019-09-11 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extendedusers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='personal_picture',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
