from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe
from pytils.translit import slugify
from django.db.models.signals import post_save

class AmoKey(models.Model):
    access_token = models.TextField(blank=True,null=True)
    refresh_token = models.TextField(blank=True,null=True)
    expires_in = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField('Название категории', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, editable=False)
    url = models.CharField('URL (для главной страницы - / , для остальных - /name)', max_length=255, blank=True, null=True, db_index=True, editable=False)

    timerDays = models.IntegerField('Сколько дней на таймере', default=1)

    offerImage = models.ImageField('Бекграунд оффера', upload_to='category/', blank=False, null=True)
    offerImageMobile = models.ImageField('Бекграунд оффера мобильный', upload_to='category/', blank=False, null=True)
    offerText = models.TextField('Текст оффера', default='Качественное турецкое постельное белье'
                                                         ' от официального диллера')
    offerDiscount = models.CharField('Текст скидки в оффере', max_length=255, default='со скидкой 30%')

    whyWeTitle = models.TextField('Заголовок блока Преймуществ', default='Посмотрите почему '
                                                                       '<span class="text-primary">постельное бельё '
                                                                       'Alanna</span> считается премиальным '
                                                                       'и почему дает здоровый и комфортный сон')
    whyWeCenterImage = models.ImageField('Картинка блока Почему мы', upload_to='category/', blank=False, null=True)
    showPromoBlock = models.BooleanField('Показывать промо блок?', default=False)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "1. Категории"


class WhyWeItem(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 on_delete=models.SET_NULL, blank=True, null=True, db_index=True,
                                 related_name='why_we_items')

    title = models.TextField('Заголовок', max_length=255, blank=False, null=True)
    text = models.TextField('Текст', max_length=255, blank=False, null=True)

    class Meta:
        verbose_name = "Преймущество"
        verbose_name_plural = "Преймущества"


class FaqItem(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 on_delete=models.SET_NULL, blank=True, null=True, db_index=True,
                                 related_name='faq_items')

    question = models.TextField('Вопрос', max_length=255, blank=False, null=True)
    answer = RichTextUploadingField('Ответ', blank=False, null=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"

class ItemSize(models.Model):
    sostav = RichTextUploadingField('Состав комплекта', blank=True, null=True)
    name = models.CharField('Размер', max_length=255, blank=True, null=True)
    price = models.FloatField('Цена', blank=True, default=0, db_index=True)
    old_price = models.FloatField('НЕ ТРОГАТЬ', blank=True, default=0, db_index=True , editable=True)
    discount = models.IntegerField('Скидка', default=0)
    is_selected = models.BooleanField(default=False, editable=False)
    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self.old_price == 0:
            self.old_price = self.price

        if self.discount > 0:
            self.old_price = self.price
            self.price = round(self.price - (self.price * self.discount / 100),2)
        else:
            self.price = self.old_price

        super(ItemSize, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "2. Размеры"





class Item(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория',
                                   on_delete=models.SET_NULL, blank=False, null=True, db_index=True,
                                   related_name='items')
    size = models.ManyToManyField(ItemSize, verbose_name='Размеры',
                                  blank=False,  db_index=True)
    image = models.ImageField('Изображение товара', upload_to='items/', blank=True)
    sostav = models.CharField('Состав', max_length=255, default='хлопок 100%')
    country = models.CharField('Производство', max_length=255, default='Турция')
    name = models.CharField('Название товара', max_length=255, blank=True, null=True)

    article = models.CharField('Артикул', max_length=50, blank=True, null=True)
    is_active = models.BooleanField('Отображать товар ?', default=True, db_index=True)
    is_present = models.BooleanField('Товар в наличии ?', default=True, db_index=True)
    is_show_at_thanks_page = models.BooleanField('Показывать на странице спасибо ?', default=False, db_index=True)
    price = models.FloatField('Цена для смтраницы спасибо', blank=True, default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    selected_size = models.IntegerField('НЕ ТРОГАТЬ', default=1, editable=True)
    ost_count = models.IntegerField(default=0, editable=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "3. Товары"

    def __str__(self):
        return f'{self.name} ({self.article})'

    def image_tag(self):

        if self.image:
            return mark_safe('<img src="{}" width="100" height="100" />'.format(self.image.url))
        else:
            return mark_safe('<span>Изображение не загружено</span>')

    def ost_tag(self):
        text=''
        ost = Ostatok.objects.filter(item=self)
        for i in ost:
            text += f'<p>{i.size.name} - <b style="color:{"red" if i.ostatok == 0 else "green"}">{i.ostatok}</b></p>'
        if text == '':
            text = '<b style="color:red">ОСТАТКИ НЕ УКАЗАНЫ</b>'
        return mark_safe(text)

    def save(self, *args, **kwargs):
        ostatki = Ostatok.objects.filter(item=self)
        for ost in ostatki:
            if ost.ostatok > 0:
                self.selected_size = ost.size.id
                break
        super(Item, self).save(*args, **kwargs)

    def selected_ost_tag(self):
        if self.selected_size>0:
            return ItemSize.objects.get(id=self.selected_size)
        else:
            return 'НЕ ВЫБРАН'

    selected_ost_tag.short_description = 'Выбранный размер'
    ost_tag.short_description = 'Остатки'
    image_tag.short_description = 'Изображение'



class Ostatok(models.Model):
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE, db_index=True, verbose_name='Товар')
    size = models.ForeignKey(ItemSize, blank=True, null=True, on_delete=models.CASCADE, db_index=True, verbose_name='Размер')
    ostatok = models.IntegerField('Остаток', default=0)
    is_size_set = models.BooleanField('НЕ ТРОГАТЬ',default=False, editable=False)

    def __str__(self):
        return f'{self.item.name}  -  {self.size.name} на остатке {self.ostatok}'

    # def save(self, *args, **kwargs):
    #     if not self.is_size_set:
    #         self.item.selected_size = self.item.size.first().id
    #         self.item.save()
    #         self.is_size_set = True
    #     super(Ostatok, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Остаток"
        verbose_name_plural = "4. Остатки"


class Feedback(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 on_delete=models.SET_NULL, blank=True, null=True, db_index=True,
                                 related_name='feedbacks')
    image = models.ImageField('Картинка отзыва', upload_to='feedback/', blank=True)
    is_active = models.BooleanField('Отображать отзыв?', default=True, db_index=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "5. Отзывы"

class CartItem(models.Model):
    session = models.CharField(max_length=255,blank=True,null=True)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE, db_index=True)
    size = models.ForeignKey(ItemSize, blank=True, null=True, on_delete=models.CASCADE, db_index=True)
    quantity = models.IntegerField('Кол-во', blank=True, null=True, default=1)
    price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.item.name}  X {self.quantity}'

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзинах"

    def save(self, *args, **kwargs):
        self.price = self.size.price * self.quantity
        super(CartItem, self).save(*args, **kwargs)


class Cart(models.Model):
    session = models.CharField(blank=True, null=True, max_length=255)
    items = models.ManyToManyField(CartItem, blank=True, verbose_name='Товары', db_index=True)
    total_price = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина  : {self.id} '

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"