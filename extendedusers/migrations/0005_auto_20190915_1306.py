# Generated by Django 2.2.4 on 2019-09-15 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extendedusers', '0004_auto_20190915_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='companyName',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
