'''
Created on 05-Jul-2014

@author: Rahul

@summary: Contains the Core Sync Service that gets the updated feeds
          from twitter and updates the same in local DB.
'''
from itertools import izip

from django.conf import settings
from tweepy import API
import tweepy
from tweepy.auth import OAuthHandler

from album.models import User, Tweet, Media, Administration
from album.utils import convert_datetime, find_max_from_collection,\
    collection_to_map


class TwitterDAO(object):
    '''
        Acts a Data Access Object (DAO) for our Sync Service.
    '''
    def __init__(self, api_key, api_key_secret, access_token, token_secret):
        '''
            Initialize the twitter API client.
        '''
        auth_handler = OAuthHandler(api_key, api_key_secret)
        auth_handler.set_access_token(access_token, token_secret)
        self.twitter_client = API(auth_handler)

    def search_updates(self, search_param, **options):
        '''
            Use the twitter client to find the updates for our search param.
        '''
        search_method = self.twitter_client.search
        users, medias, tweets = [], [], []

        # Prepare our model objects for all the new tweets.
        for tweet in tweepy.Cursor(search_method, search_param, **options).items():  # @IgnorePep8
            users.append(self._get_user(tweet))
            medias.append(self._get_medias(tweet))
            tweets.append(self._get_tweet(tweet))

        return users, medias, tweets

    def _get_user(self, tweet_model):
        '''
            Prepares and returns the user model.
        '''
        user = tweet_model.user
        return User(id=user.id_str, name=user.screen_name,
                    friends=user.friends_count,
                    followers=user.followers_count)

    def _get_medias(self, tweet_model):
        '''
            Prepares and returns the media models.
        '''
        media_entities = (tweet_model.entities or {}).get("media", [])

        def construct_media(me):
            return Media(id=me.get("id_str"), type=me.get("type"),
                         media_url_https=me.get("media_url_https"),
                         media_url_http=me.get("media_url"))

        return [construct_media(me) for me in media_entities]

    def _get_tweet(self, tweet_model):
        '''
            Prepares and returns the tweet model.
        '''
        created_at = convert_datetime(tweet_model.created_at)
        geo_cords = (tweet_model.geo or {}).get("coordinates", [0.0, 0.0])

        return Tweet(id=tweet_model.id_str, long=geo_cords[1], lat=geo_cords[0],  # @IgnorePep8
                     created_at=created_at, retweets=tweet_model.retweet_count,
                     lang=tweet_model.lang, text=tweet_model.text)


class LocalDAO(object):
    '''
        Handles updating the local DB with the updated feeds.
        All the method defined here are using bulk upserts whenever possible
        to avoid standard N+1 problem.
    '''
    @classmethod
    def update_users(cls, users):
        '''
            Sync the user information received from twitter into local DB.
        '''
        key_attr = "id"
        update_fields = ["name"]

        # Remove duplicates.
        updated_users = collection_to_map(users, key_attr).values()

        return User.objects.all().bulk_upsert(updated_users, [key_attr],
                                              update_fields, True)

    @classmethod
    def update_medias(cls, medias, tweets, unique_tweets):
        '''
            Sync the media information received from twitter into local DB.
        '''
        key_attr = "id"
        flatten_medias = []
        media_tweet_mapping = {}

        # Flattens the list of lists into a single list.
        for tweet, media in izip(tweets, medias):
            unq_obj = unique_tweets.get(tweet.id)
            media_tweet_mapping.update(dict([(m.id, unq_obj) for m in media]))
            flatten_medias.extend(media)

        # Remove duplicates.
        flatten_medias = collection_to_map(flatten_medias, key_attr).values()

        # Persist all the media objects without relationship.
        saved_medias = Media.objects.bulk_upsert(flatten_medias, [key_attr],
                                                 None, True)

        # lets now set the relationship for medias and tweets.
        # FIXME: This still results in N queries. Not a good support
        # available for persisting Many to Many relationships.
        for saved_media in saved_medias:
            saved_media.tweets.add(media_tweet_mapping.get(saved_media.id))

    @classmethod
    def update_tweets(cls, users, tweets, unique_users):
        '''
            Sync the tweets information received from twitter into local DB.
        '''
        key_attr = "id"
        update_fields = ["retweets"]

        # Add user -> tweet relationship.
        for tweet, user in izip(tweets, users):
            tweet.user = unique_users.get(user.id)

        # Remove duplicates
        tweets = collection_to_map(tweets, key_attr).values()

        return Tweet.objects.bulk_upsert(tweets, [key_attr], update_fields,
                                         True)

    @classmethod
    def get_max_id(cls, start_max_id):
        '''
            Gets the last successfully saved tweet id.
        '''
        get_admin = Administration.objects.get_or_create
        defaults = {"max_id": start_max_id}
        obj, created = get_admin(id=1, defaults=defaults)  # @UnusedVariable
        return obj.max_id

    @classmethod
    def update_max_id(cls, max_id):
        '''
            Updates the max_id of to a given value.
        '''
        Administration.objects.update()
        obj = Administration.objects.get(id=1)
        obj.max_id = max_id
        obj.save()
        return obj.max_id

    @classmethod
    def get_media_count(cls):
        '''
            Updates the max_id of to a given value.
        '''
        return Media.objects.count()


class SyncService(object):
    '''
        Service that find updates using twitter APIs and updates the local DB.
    '''
    @classmethod
    def sync(cls):
        '''
            looks for updates through twitter DAO and updates the local DB.
        '''
        creds = settings.TWITTER_CREDS
        search_param = settings.SEARCH_PARAM
        start_max_id = settings.START_MAX_ID
        users_key_attr = tweets_key_attr = "id"

        twitter_dao = TwitterDAO(creds["API_KEY"], creds["API_SECRET"],
                                 creds["ACCESS_TOKEN"],
                                 creds["ACCESS_TOKEN_SECRET"])
        max_id = LocalDAO.get_max_id(start_max_id)

        users, medias, tweets = twitter_dao.search_updates(search_param,
                                                           since_id=max_id,
                                                           count=100)

        updated_max = find_max_from_collection(tweets, "id")

        # Persist all our entities.
        u_users = LocalDAO.update_users(users)
        u_users_map = collection_to_map(u_users, users_key_attr)

        u_tweets = LocalDAO.update_tweets(users, tweets, u_users_map)
        u_tweets_map = collection_to_map(tweets, tweets_key_attr)

        u_medias = LocalDAO.update_medias(medias, u_tweets,  # @UnusedVariable
                                          u_tweets_map)
        # All the entities saved, now update the max id for next run.
        LocalDAO.update_max_id(updated_max)

        return LocalDAO.get_media_count()
