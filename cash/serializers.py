from .models import User, Product, Shop, Shopping, Invoice, Notification
from rest_framework import serializers


class SignSerializer(serializers.ModelSerializer):
    model = User
    fields = (
        'phone'
    )

    def to_representation(self, instance):
        notifies = Notification.objects.filter(destinate=instance)
        return {
            'id': instance.id,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'phone': instance.phone,
            'email': instance.email,
            'role': instance.role,
            'country': instance.country,
            'state': instance.state,
            'city': instance.city,
            # 'picture': instance.picture,
            'fringerprint': instance.fringerprint,
            'notifications': NotifySerializer(notifies, many=True).data,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        } | {
            'code': instance.code,
            'qrcode': instance.qrcode
        } if instance.code else {}


class FringerSignSerializer(serializers.ModelSerializer):
    model = User
    fields = (
        'fringerprint'
    )

    def to_representation(self, instance):
        notifies = Notification.objects.filter(destinate=instance)
        return {
            'id': instance.id,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'phone': instance.phone,
            'email': instance.email,
            'role': instance.role,
            'country': instance.country,
            'state': instance.state,
            'city': instance.city,
            # 'picture': instance.picture,
            'fringerprint': instance.fringerprint,
            'notifications': NotifySerializer(notifies, many=True).data,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        } | {
            'code': instance.code,
            'qrcode': instance.qrcode
        } if instance.code else {}


class UserSerializer(serializers.ModelSerializer):
    model = User
    fields = '__all__'

    def to_representation(self, instance):
        notifies = Notification.objects.filter(destinate=instance)
        return {
            'id': instance.id,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'phone': instance.phone,
            'email': instance.email,
            'role': instance.role,
            'country': instance.country,
            'state': instance.state,
            'city': instance.city,
            # 'picture': instance.picture,
            'fringerprint': instance.fringerprint,
            'notifications': NotifySerializer(notifies, many=True).data,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        } | {
            'code': instance.code,
            'qrcode': instance.qrcode
        } if instance.code else {}


class ProductSerialzer(serializers.ModelSerializer):
    model = Product
    fields = (
        'name',
        'description',
        'price',
        'unit'
    )

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'marchand': instance.marchand.code,
            'name': instance.name,
            'picture': instance.picture,
            'price': instance.price,
            'unit': instance.unit,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }


class ShoppingSerializer(serializers.ModelSerializer):
    model = Shopping
    fields = (
        'qte',
        'price'
    )

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'client': instance.client.phone,
            'product': {
                'name': instance.product.name,
                'picture': instance .product.picture,
                'price': instance.product.price,
                'unit': instance.product.unit
            },
            'qte': instance.qte,
            'price': instance.price,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }


class ShopSerializer(serializers.ModelSerializer):
    model = Shop

    def to_representation(self, instance):
        products = Shopping.objects.filter(shop=instance)
        prices = sum([p.price for p in products])
        return {
            'id': instance.id,
            'client': instance.client.phone,
            'products': ShoppingSerializer(products, many=True).data,
            'shop_price': prices,
            'fees': prices * 0.05,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }


class InvoiceSerializer(serializers.ModelSerializer):
    model = Invoice

    def to_representation(self, instance):
        shop = ShopSerializer(instance.shop).data
        return {
            'ref': instance.id,
            'marchand': instance.marchand.code,
            'client': instance.client.phone,
            'shop': shop,
            'price': shop['shop_price'] + shop['fees'],
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }


class NotifySerializer(serializers.ModelSerializer):
    model = Notification

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'destinate': instance.destinate.phone,
            'message': instance.message,
            'read': instance.read,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at
        }
