from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class UserSerializer(ModelSerializer):
    """Сериализатор по пользователям"""

    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    """Сериализатор по платежам"""

    class Meta:
        model = Payment
        fields = "__all__"
