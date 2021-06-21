from .models        import *
from rest_framework import serializers

class PaymentRegisterSerializer(serializers.Serializer):
    orderer           = serializers.CharField(help_text="주문자")
    orderer_contact   = serializers.CharField(help_text="주문자 연락처")
    recipient         = serializers.CharField(help_text="배송 받는 사람 이름")
    recipient_contact = serializers.CharField(help_text="배송 받는 사함 연락처")
    address           = serializers.CharField(help_text="주소")
    payment           = serializers.CharField(help_text="결제타입")
    option            = serializers.CharField(help_text=[{"option_id": 1, "title": "상품1", "price": 1000, "quantity": 1, "stock": 20},
    {"option_id": 1, "title": "상품1", "price": 1000, "quantity": 1, "stock": 20}])
    request           = serializers.CharField(help_text="요청사항")