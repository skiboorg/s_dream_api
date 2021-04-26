from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMessage
import settings


def check_if_cart_exists(session_id):
    cart, created = Cart.objects.get_or_create(session=session_id)
    if created:
        print('new cart created')
    else:
        print('cart already created')
    return cart


class ItemsPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response({
            'links':{
                'next': self.get_next_link(),
                'prev': self.get_previous_link(),
            },
            'page_count':self.page.paginator.num_pages,
            'results':data
        })



class GetCats(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GetItems(APIView):

    pagination_class = ItemsPagination
    def get(self,request):
        items = Item.objects.filter(category__name_slug=self.request.query_params.get('cat_slug'),is_active=True)
        bad_items = []
        for i in items:
            has_ost = False
            ost = Ostatok.objects.filter(item=i)
            for o in ost:
                if o.ostatok > 0:
                    has_ost = True
            if not  has_ost:
                bad_items.append(i.id)
        items = items.exclude(id__in=bad_items)
        page = self.paginate_queryset(items)
        if page is not None:
            serializer = ItemSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)



class GetOstatok(generics.ListAPIView):
    serializer_class = OstatokSerializer
    def get_queryset(self):
        return Ostatok.objects.filter(item__category__name_slug=self.request.query_params.get('cat_slug'))


class GetCart(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    def get_object(self):
        cart = check_if_cart_exists(self.request.query_params.get('session_id'))
        return cart

class AddToCart(APIView):
    def post(self,request):
        print(request.data)
        data = request.data
        item_id = data.get('item_id')
        size_id = data.get('size_id')
        session = data.get('session_id')
        cart = check_if_cart_exists(session)
        try:
            cart_item = CartItem.objects.get(
                session=session,
                item_id=item_id,
                size_id=size_id)
            cart_item.quantity += 1
            cart_item.save()

        except CartItem.DoesNotExist:
            new_cart_item = CartItem.objects.create(
                session=session,
                item_id=item_id,
                size_id=size_id,
                quantity=1)
            cart.items.add(new_cart_item)

        return Response(status=200)


class DeleteItem(APIView):
    def post(self, request):
        data = request.data
        print(data)
        item_id = data.get('item_id')
        size_id = data.get('size_id')
        session = data.get('session_id')
        cart_item = CartItem.objects.get(
            session=session,
            item_id=item_id,
            size_id=size_id)
        cart_item.delete()
        return Response(status=200)


class PlusQuantity(APIView):
    def post(self, request):
        data = request.data
        print(data)
        item_id = data.get('item_id')
        size_id = data.get('size_id')
        session = data.get('session_id')
        cart_item = CartItem.objects.get(
            session=session,
            item_id=item_id,
            size_id=size_id)
        cart_item.quantity += 1
        cart_item.save()
        return Response(status=200)


class MinusQuantity(APIView):
    def post(self, request):
        data = request.data
        print(data)
        item_id = data.get('item_id')
        size_id = data.get('size_id')
        session = data.get('session_id')
        cart_item = CartItem.objects.get(
            session=session,
            item_id=item_id,
            size_id=size_id)
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()
        return Response(status=200)

class SendMail(APIView):
    def post(self,request):
        data = request.data
        print(data)
        html = None
        type = None
        if data.get('type') == 'callback':
            type = 'Обратный звонок'
            html = render_to_string('callBack.html',
                                    {
                                        'name':data.get('data')['name'],
                                        'phone':data.get('data')['phone'],
                                    })
        if data.get('type') == 'quiz':
            type = 'Квиз'
            html = render_to_string('quiz.html',
                                    {
                                        'name':data.get('data')['name'],
                                        'phone':data.get('data')['phone'],
                                        'quiz':data.get('data')['quiz'],
                                    })
        if data.get('type') == 'order':
            type = 'Заказ'
            cart = check_if_cart_exists(data.get('data')['session_id'])
            items = cart.items.all()
            html = render_to_string('order.html',
                                    {
                                        'name': data.get('data')['name'],
                                        'phone': data.get('data')['phone'],
                                        'items': items,
                                        'cart':cart
                                    })
            for i in cart.items.all():
                ostatok = Ostatok.objects.get(item=i.item,size=i.size)
                print(ostatok)
                if ostatok.ostatok - i.quantity < 0:
                    ostatok.ostatok = 0
                else:
                    ostatok.ostatok -= i.quantity
                ostatok.save()
            items.delete()

        send_mail(type, None, settings.MAIL_TO, (settings.MAIL_TO,'ToYou.work@yandex.by',),
                   fail_silently=False, html_message=html)

        return Response(status=200)
