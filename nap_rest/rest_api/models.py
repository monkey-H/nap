from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Service(models.Model):
    """
    model for users' service in nap
    """
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    origin_url = models.CharField(max_length=200)
    instance_num = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('created',)


class App(models.Model):
    """
    model for users' app in nap
    """
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    port = models.PositiveSmallIntegerField(default=0)
    cat = models.TextField()
    state = models.CharField(max_length=100)
    sub = models.CharField(max_length=100)
    journal = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='apps')
    service = models.ForeignKey(Service, related_name='app')

    class Meta:
        ordering = ('created',)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    ensure every user to have an automatically generated Token
    catch user's post save signal
    """
    if created:
        Token.objects.create(user=instance)
