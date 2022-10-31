from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
     description = models.CharField(verbose_name="description", null=False, blank=False, max_length=200)
     image = models.ImageField(verbose_name="Photo", null=False, blank=False)
     author = models.ForeignKey(verbose_name="author", to=get_user_model(), related_name="posts", null=False,
                                blank=False, on_delete=models.CASCADE)



class Comment(models.Model):
    author = models.ForeignKey(verbose_name="author", to=get_user_model(), related_name="comments", null=False,
                               blank=False, on_delete=models.CASCADE)
    post = models.ForeignKey(verbose_name="author", to="posts.Post", related_name="comments", null=False,
                               blank=False, on_delete=models.CASCADE)
    text = models.CharField(verbose_name="description", null=False, blank=False, max_length=200)


# class Like(models.Model):
#     liked_by = models.ForeignKey(verbose_name="Who liked", to=get_user_model(), related_name="likes", null=False,
#                                blank=False, on_delete=models.CASCADE)
#     post = models.ForeignKey(verbose_name="Who liked", to=get_user_model(), related_name="likes", null=False,
#                                  blank=False, on_delete=models.CASCADE)