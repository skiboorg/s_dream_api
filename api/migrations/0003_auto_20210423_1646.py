# Generated by Django 3.2 on 2021-04-23 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210423_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='selected_size',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='ostatok',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.item', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='ostatok',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.itemsize', verbose_name='Размер'),
        ),
    ]
