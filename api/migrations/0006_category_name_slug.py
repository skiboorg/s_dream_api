# Generated by Django 3.2 on 2021-04-24 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210424_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_slug',
            field=models.CharField(blank=True, editable=False, max_length=255, null=True),
        ),
    ]
