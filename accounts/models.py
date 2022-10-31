from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager


class Account(AbstractUser):
    email = models.EmailField(verbose_name="Email", unique=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="Profile picture")
    birthday = models.DateField(null=True, blank=True, verbose_name="Date of birth")
    objects = UserManager()
    liked_posts = models.ManyToManyField(to="posts.Post", related_name="user_likes")
    subscriptions = models.ManyToManyField(to="accounts.Account", related_name="subscribers")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"



