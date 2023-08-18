from re import U
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .serializers import UrlDetailSerializer, RegisterSerializer, TokenSerializer

from .models import UrlDetail
from .utils import ShortUrl


@api_view(["GET"])
def get_url(request):
    s_url = request.GET.get("s_url", "")
    if not s_url:
        return Response({"message": f"short url {s_url} not found."}, status=404)

    long_url = get_object_or_404(UrlDetail, short_url=s_url)
    serializer = UrlDetailSerializer(long_url)
    return Response(serializer.data)


@api_view(["POST"])
def generate_url(request):
    is_url_present = False
    data = request.data
    token = request.META.get("HTTP_AUTHORIZATION")
    user_id = Token.objects.filter(key=token).values_list("user", flat=True)[0]
    data["user"] = user_id
    long_url = data.get("long_url", "")
    if not long_url:
        return Response({"message": "long_url key is required"}, status=400)
    try:
        url = UrlDetail.objects.get(long_url=long_url, user=user_id)
        is_url_present = True
    except UrlDetail.DoesNotExist:
        short_url = ShortUrl.generate_short_url(data["long_url"])
    if is_url_present:
        serializer = UrlDetailSerializer(url)
        return Response(serializer.data, status=302)
    data["short_url"] = short_url
    serializer = UrlDetailSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors)


@api_view(["GET"])
def get_all_urls(request):
    token_key = request.META.get("HTTP_AUTHORIZATION")
    user = Token.objects.get(key=token_key).user
    all_urls = UrlDetail.objects.filter(user=user)
    serializer = UrlDetailSerializer(all_urls, many=True)
    return Response(serializer.data)


def go_to_url(request, short_url):
    try:
        url = get_object_or_404(UrlDetail, short_url=short_url)
    except Http404:
        return HttpResponse("invalid url")
    return HttpResponseRedirect(url.long_url)


@api_view(["POST"])
def get_token(request):
    data = request.data
    serializer = TokenSerializer(data=data)
    if serializer.is_valid():
        user = serializer.validated_data["user_id"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "username": serializer.validated_data["username"],
                "email": serializer.validated_data["email"],
            }
        )

    return Response(serializer.errors)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
