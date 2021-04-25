# Generated by Django 3.2 on 2021-04-25 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20210425_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='api.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='item',
            name='size',
            field=models.ManyToManyField(db_index=True, to='api.ItemSize', verbose_name='Размеры'),
        ),
    ]