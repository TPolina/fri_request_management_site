# Generated by Django 3.2.7 on 2021-12-03 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fri_site', '0002_auto_20211129_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='responsible',
            field=models.CharField(max_length=64, null=True),
        ),
    ]