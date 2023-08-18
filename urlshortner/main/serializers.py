from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import UrlDetail
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class UrlDetailSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(
        validators=[UniqueValidator(queryset=UrlDetail.objects.all())]
    )
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UrlDetail
        fields = ("long_url", "short_url", "user", "created_at")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=UrlDetail.objects.all(),
                fields=("long_url", "user"),
                message=_(
                    "you have already genereted short url for this long url hello world"
                ),
            )
        ]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid Username or Password")
        data["email"] = user.email
        data["user_id"] = user
        return data
