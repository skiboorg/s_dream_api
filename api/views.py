from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMessage
from datetime import datetime
import requests
import datetime as dt
from datetime import datetime
from django.utils import timezone

import settings

def get_amo_key():
    print('Checking access_token.........')
    token = AmoKey.objects.first()
    if (timezone.now() - token.updated_at).total_seconds() < token.expires_in:
        print('Access_token is ok')
        return token.access_token

    else:
        print(f'{datetime.now()} - Changing access_token')
        headers = {
            'Content-Type': 'application/json',
        }
        data = {"client_id": settings.AMO_ID, "client_secret": settings.AMO_SECRET, "grant_type": "refresh_token",
                "refresh_token": token.refresh_token,
                "redirect_uri": "https://sweet-dreams.by/"}
        response = requests.post('https://toyou.amocrm.ru/oauth2/access_token', headers=headers,
                                 json=data)
        print(f'{datetime.now()} - AMO response')
        print(response.json())
        token.access_token = response.json()['access_token']
        token.refresh_token = response.json()['refresh_token']
        token.expires_in = response.json()['expires_in']
        token.save()
        print(f'{datetime.now()} - Changing access_token successful')
        return response.json()['access_token']


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


def send_amo_info(name,phone,fio):
    token = get_amo_key()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token

    }
    data = [
        {
        'pipeline_id' : 1371766,
        'name': name,
        "custom_fields_values": [
            {
                "field_id": 62779,
                "values": [
                    {
                        "value": fio
                    }
                ]
            },
            {
                "field_id": 62781,
                "values": [
                    {
                        "value": phone
                    }
                ]
            }
        ]
        }
    ]
    response = requests.post('https://toyou.amocrm.ru/api/v4/leads', headers=headers,
                             json=data)
    print(response.json())
    return


class GetItemsForThanks(APIView):
    pagination_class = ItemsPagination
    def get(self,request):
        items = Item.objects.filter(is_show_at_thanks_page=True)
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
            send_amo_info('Обратный звонок', data.get('data')['phone'], data.get('data')['name'])
        if data.get('type') == 'quiz':
            type = 'Квиз'
            html = render_to_string('quiz.html',
                                    {
                                        'name':data.get('data')['name'],
                                        'phone':data.get('data')['phone'],
                                        'quiz':data.get('data')['quiz'],
                                    })
            send_amo_info('Квиз', data.get('data')['phone'], data.get('data')['name'])
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
            zakaz = ''
            for i in cart.items.all():
                zakaz += f'{i.item.name} ({i.item.article}) x {i.quantity}шт, '
                ostatok = Ostatok.objects.get(item=i.item,size=i.size)
                print(ostatok)
                if ostatok.ostatok - i.quantity < 0:
                    ostatok.ostatok = 0
                else:
                    ostatok.ostatok -= i.quantity
                ostatok.save()
            items.delete()

            send_amo_info(zakaz, data.get('data')['phone'], data.get('data')['name'])

        send_mail(type, None, settings.MAIL_TO, (settings.MAIL_TO,'ToYou.work@yandex.by',),
                   fail_silently=False, html_message=html)

        return Response(status=200)
