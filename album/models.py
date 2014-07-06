from django.db import models
from django.conf import settings
from manager_utils.manager_utils import ManagerUtilsManager

APP_LABEL = settings.APP_LABEL


class User(models.Model):
    '''
        Represents the User entry.
    '''
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    friends = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    objects = ManagerUtilsManager()

    class Meta:
        app_label = APP_LABEL
        db_table = app_label + "_users"


class Tweet(models.Model):
    '''
        Represents a tweet entry. The id field value is determined by tweet id.
    '''
    id = models.CharField(max_length=20, primary_key=True)
    created_at = models.DateTimeField()
    retweets = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=150)
    lat = models.FloatField(null=True)
    long = models.FloatField(null=True)
    lang = models.CharField(max_length=3, null=True)
    objects = ManagerUtilsManager()

    class Meta:
        app_label = APP_LABEL
        db_table = app_label + "_tweets"


class Media(models.Model):
    '''
        Represents the Media entry for a particular tweet.
    '''
    id = models.CharField(max_length=20, primary_key=True)
    media_url_http = models.CharField(max_length=200)
    media_url_https = models.CharField(max_length=200)
    type = models.CharField(max_length=20)
    tweets = models.ManyToManyField(Tweet)
    objects = ManagerUtilsManager()

    class Meta:
        app_label = APP_LABEL
        db_table = app_label + "_medias"


class Administration(models.Model):
    '''
        The only need of this right now is to save the last successfully
        updated tweet. Value of this would be used as a since_id param while
        querying twitter for updates.
    '''
    max_id = models.CharField(max_length=20)
    objects = ManagerUtilsManager()

    class Meta:
        app_label = APP_LABEL
        db_table = app_label + "_administration"
