from django.contrib import admin
from .models import *

class WhyWeItemInline (admin.TabularInline):
    model = WhyWeItem
    extra = 0

class FaqItemInline (admin.TabularInline):
    model = FaqItem
    extra = 0

class FeedbackInline (admin.TabularInline):
    model = Feedback
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    inlines = [WhyWeItemInline,FaqItemInline,FeedbackInline]
    class Meta:
        model = Category

class OstatokInline (admin.TabularInline):
    model = Ostatok
    extra = 0

class OstatokAdmin(admin.ModelAdmin):
    list_filter = ('item',)

    class Meta:
        model = Ostatok

class ItemAdmin(admin.ModelAdmin):
    list_display = ['image_tag','name', 'article', 'is_active','ost_tag']
    inlines = [OstatokInline]
    list_filter = ('is_active','category','size',)
    class Meta:
        model = Item

admin.site.register(Category,CategoryAdmin)
admin.site.register(ItemSize)
admin.site.register(Ostatok,OstatokAdmin)
# admin.site.register(ItemComplect)
admin.site.register(Item,ItemAdmin)

