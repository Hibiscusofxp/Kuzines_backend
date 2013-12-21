from django.db import models

# Create your models here.

class Locations(models.Model):
    lid = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=200L, blank=True)
    city = models.CharField(max_length=50L, blank=True)
    state = models.CharField(max_length=50L, blank=True)
    country = models.CharField(max_length=50L, blank=True)
    class Meta:
        db_table = 'locations'

class Users(models.Model):
    uid = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=100L)
    lastname = models.CharField(max_length=100L, blank=True)
    username = models.CharField(max_length=100L, unique=True)
    password = models.CharField(max_length=256L)
    birthday = models.DateField(null=True, blank=True)
    location = models.ForeignKey(Locations, null=True, db_column='location', blank=True)
    class Meta:
        db_table = 'users'


class Posts(models.Model):
    ptid = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=2000L)
    time = models.DateField()
    location = models.ForeignKey(Locations, null=True, db_column='location', blank=True)
    user = models.ForeignKey(Users, null=True, db_column='user', blank=True)
    class Meta:
        db_table = 'posts'


class Restaurants(models.Model):
    rid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200L)
    type = models.CharField(max_length=50L, blank=True)
    visits = models.IntegerField(null=True, blank=True)
    favorited = models.IntegerField(null=True, blank=True)
    location = models.ForeignKey(Locations, null=True, db_column='location', blank=True)
    class Meta:
        db_table = 'restaurants'

class Dishes(models.Model):
    did = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200L)
    dscp = models.CharField(max_length=2000L, blank=True)
    restaurant = models.ForeignKey(Restaurants, null=True, db_column='restaurant', blank=True)
    numtries = models.IntegerField(null=True, blank=True)
    numlikes = models.IntegerField(null=True, blank=True)
    numtopdish = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'dishes'

class Photos(models.Model):
    pid = models.IntegerField(primary_key=True)
    link = models.CharField(max_length=200L, unique=True, blank=True)
    author = models.ForeignKey(Users, null=True, db_column='author', blank=True)
    restaurant = models.ForeignKey(Restaurants, null=True, db_column='restaurant', blank=True)
    class Meta:
        db_table = 'photos'


# -- RELATIONS

class Favrestaurants(models.Model):
    uid = models.ForeignKey(Users, db_column='uid')
    rid = models.ForeignKey(Restaurants, db_column='rid')
    class Meta:
        db_table = 'favrestaurants'

class Favdishes(models.Model):
    uid = models.ForeignKey(Users, db_column='uid')
    did = models.ForeignKey(Dishes, db_column='did')
    class Meta:
        db_table = 'favdishes'

class Checkins(models.Model):
    uid = models.ForeignKey(Users, db_column='uid')
    rid = models.ForeignKey(Restaurants, db_column='rid')
    class Meta:
        db_table = 'checkins'

class Usertags(models.Model):
    uid = models.ForeignKey(Users, db_column='uid')
    pid = models.ForeignKey(Photos, db_column='pid')
    class Meta:
        db_table = 'usertags'

class Dishtags(models.Model):
    did = models.ForeignKey(Dishes, db_column='did')
    pid = models.ForeignKey(Photos, db_column='pid')
    class Meta:
        db_table = 'dishtags'

class Reviews(models.Model):
    uid = models.ForeignKey(Users, db_column='uid')
    did = models.ForeignKey(Dishes, db_column='did')
    level = models.IntegerField(null=True, blank=True)
    dscp = models.CharField(max_length=2000L, blank=True)
    class Meta:
        db_table = 'reviews'

class Likes(models.Model):
    uid = models.ForeignKey(Users, db_column='uid')
    did = models.ForeignKey(Dishes, db_column='did')
    class Meta:
        db_table = 'likes'

class Friends(models.Model):
    user1 = models.ForeignKey(Users, related_name='friends1')
    user2 = models.ForeignKey(Users, related_name='friends2')
    class Meta:
        db_table = 'friends'

class Tries(models.Model):
    uid = models.ForeignKey(Users, db_column='uid')
    did = models.ForeignKey(Dishes, db_column='did')
    class Meta:
        db_table = 'tries'
