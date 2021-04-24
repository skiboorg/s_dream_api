from django.contrib import admin
from .models import *

class WhyWeItemInline (admin.TabularInline):
    model = WhyWeItem
    extra = 0

class FaqItemInline (admin.TabularInline):
    model = FaqItem
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    inlines = [WhyWeItemInline,FaqItemInline]
    class Meta:
        model = Category
class ItemAdmin(admin.ModelAdmin):
    list_display = ['image_tag','name', 'article', 'is_active']
    # inlines = [ImagesInline]
    list_filter = ('is_active',)
    class Meta:
        model = Item

admin.site.register(Category,CategoryAdmin)
admin.site.register(ItemSize)
admin.site.register(Ostatok)
admin.site.register(Cart)
admin.site.register(CartItem)
# admin.site.register(ItemComplect)
admin.site.register(Item,ItemAdmin)