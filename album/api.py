'''
Created on 05-Jul-2014

@author: Rahul

@summary: Holds all the REST resources for our application.
          Since we don't need to create users from external environment,
          through POST request, resources only supports GET verb.
'''
from tastypie.resources import ModelResource
from album.models import User, Media, Tweet
from tastypie import fields
from django.forms.models import model_to_dict


class AppSpecificModelResource(ModelResource):
    '''
        Holds common extensions to standard functionality provided by
        ModelResource.
    '''
    class Meta:
        allowed_methods = ['get']


class UserResource(AppSpecificModelResource):
    '''
        Represents the REST resource for user entity.
    '''
    class Meta(AppSpecificModelResource.Meta):
        queryset = User.objects.all()
        resource_name = "users"


class MediaResource(AppSpecificModelResource):
    '''
        Represents the REST resource for user entity.
    '''
    class Meta(AppSpecificModelResource.Meta):
        queryset = Media.objects.all()
        resource_name = "medias"
        ordering = ["id"]


class TweetResource(AppSpecificModelResource):
    '''
        Represents the REST resource for user entity.
    '''
    user = fields.ForeignKey(UserResource, "user", full=True)
    medias = fields.ManyToManyField(MediaResource, "media_set", null=True)

    class Meta(AppSpecificModelResource.Meta):
        queryset = Tweet.objects.all()
        resource_name = "tweets"

    def dehydrate_medias(self, bundle):
        """
            Resolves the reverse relationship of media -> tweets.
        """
        # FIXME: Handle resource URIs properly.
        objects = getattr(getattr(bundle.obj, "media_set"), "all")()
        fields = ["id", "media_url_http", "media_url_https", "type"]
        return [model_to_dict(obj, fields=fields) for obj in objects]
