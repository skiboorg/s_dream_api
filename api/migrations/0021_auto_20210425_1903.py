# Generated by Django 3.2 on 2021-04-25 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20210425_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemsize',
            name='discount',
            field=models.IntegerField(default=0, verbose_name='Скидка'),
        ),
        migrations.AddField(
            model_name='itemsize',
            name='old_price',
            field=models.FloatField(blank=True, db_index=True, default=0, verbose_name='НЕ ТРОГАТЬ'),
        ),
        migrations.AlterField(
            model_name='item',
            name='selected_size',
            field=models.IntegerField(default=1, verbose_name='НЕ ТРОГАТЬ'),
        ),
        migrations.AlterField(
            model_name='ostatok',
            name='is_size_set',
            field=models.BooleanField(default=False, verbose_name='НЕ ТРОГАТЬ'),
        ),
    ]
