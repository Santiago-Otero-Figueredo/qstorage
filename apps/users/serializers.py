from rest_framework import serializers 
from rest_framework.exceptions import ValidationError

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password"} ,write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password', 'password2')
        extra_kwargs = {
            "password":{"write_only": True}
        }


    def validate(self, data):

        if data['password'] != data['password2']:
            raise ValidationError("The passwords must be the same")

        if User.objects.filter(email=data['email']).exists():
            raise ValidationError("This email already a user registered with tat email")

        data.pop("password2")

        return data


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user