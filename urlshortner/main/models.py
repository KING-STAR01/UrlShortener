from django.db import models
from django.contrib.auth.models import User


class UrlDetail(models.Model):
    long_url = models.CharField(max_length=512, blank=False, null=False, db_index=True)
    short_url = models.CharField(max_length=7, primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)

    def __repr__(self) -> str:
        return f"{self.short_url} --- {self.long_url}"

    def __str__(self) -> str:
        return f"{self.short_url}"


class IncrementalNumber(models.Model):
    short_url = models.BigIntegerField(default=100000000000)
