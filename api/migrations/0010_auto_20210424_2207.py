# Generated by Django 3.2 on 2021-04-24 19:07

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_category_timerdays'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faqitem',
            options={'verbose_name': 'FAQ', 'verbose_name_plural': 'FAQ'},
        ),
        migrations.AlterModelOptions(
            name='whyweitem',
            options={'verbose_name': 'Преймущество', 'verbose_name_plural': 'Преймущества'},
        ),
        migrations.AlterField(
            model_name='category',
            name='url',
            field=models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True, verbose_name='URL (для главной страницы - / , для остальных - /name)'),
        ),
        migrations.AlterField(
            model_name='category',
            name='whyWeTitle',
            field=models.TextField(default='Посмотрите почему <span class="text-primary">постельное бельё Alanna</span> считается премиальным и почему дает здоровый и комфортный сон', verbose_name='Заголовок блока Преймуществ'),
        ),
        migrations.AlterField(
            model_name='faqitem',
            name='answer',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Ответ'),
        ),
        migrations.AlterField(
            model_name='faqitem',
            name='question',
            field=models.TextField(max_length=255, null=True, verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='whyweitem',
            name='text',
            field=models.TextField(max_length=255, null=True, verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='whyweitem',
            name='title',
            field=models.TextField(max_length=255, null=True, verbose_name='Заголовок'),
        ),
    ]