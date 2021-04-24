# Generated by Django 3.2 on 2021-04-24 11:37

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_category_name_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='offerDiscount',
            field=models.CharField(default='со скидкой 30%', max_length=255, verbose_name='Текст скидки в оффере'),
        ),
        migrations.AddField(
            model_name='category',
            name='offerImage',
            field=models.ImageField(null=True, upload_to='category/', verbose_name='Бекграунд оффера'),
        ),
        migrations.AddField(
            model_name='category',
            name='offerText',
            field=models.TextField(default='Посмотрите почему <span class="text-primary">постельное бельё Alanna</span> считается премиальным и почему дает здоровый и комфортный сон', verbose_name='Текст оффера'),
        ),
        migrations.AddField(
            model_name='category',
            name='whyWeCenterImage',
            field=models.ImageField(null=True, upload_to='category/', verbose_name='Картинка блока Почему мы'),
        ),
        migrations.AddField(
            model_name='category',
            name='whyWeTitle',
            field=models.TextField(default='Посмотрите почему <span class="text-primary">постельное бельё Alanna</span> считается премиальным и почему дает здоровый и комфортный сон', verbose_name='Заголовок блока Почему мы'),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='api.category', verbose_name='Категория'),
        ),
        migrations.CreateModel(
            name='WhyWeItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Заголовок')),
                ('text', models.CharField(max_length=255, null=True, verbose_name='Текст')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='why_we_items', to='api.category', verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='FaqItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255, null=True, verbose_name='Вопрос')),
                ('answer', ckeditor_uploader.fields.RichTextUploadingField(max_length=255, null=True, verbose_name='Ответ')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='faq_items', to='api.category', verbose_name='Категория')),
            ],
        ),
    ]
