from django.db import models


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    like_posts = models.ManyToManyField('Post', blank=True, related_name='liking_person')


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.OneToOneField('Person', on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=10)


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    likes = models.IntegerField(default=0)
    created_by = models.ForeignKey('Person', related_name='created_posts', on_delete=models.RESTRICT)
