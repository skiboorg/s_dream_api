from django.urls import path,include
from . import views

urlpatterns = [
    path('get_cats', views.GetCats.as_view()),
    path('get_items', views.GetItems.as_view()),
    path('get_ost', views.GetOstatok.as_view()),
    path('get_cart', views.GetCart.as_view()),
    path('add_to_cart', views.AddToCart.as_view()),
    path('delete_item', views.DeleteItem.as_view()),
    path('plus_quantity', views.PlusQuantity.as_view()),
    path('minus_quantity', views.MinusQuantity.as_view()),
    path('send_mail', views.SendMail.as_view()),



]
