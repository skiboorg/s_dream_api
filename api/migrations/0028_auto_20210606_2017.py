# Generated by Django 3.2 on 2021-06-06 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_item_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='ost_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ostatok',
            name='is_size_set',
            field=models.BooleanField(default=False, editable=False, verbose_name='НЕ ТРОГАТЬ'),
        ),
    ]
