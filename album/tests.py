from tastypie.test import ResourceTestCase
from django.conf import settings


class BaseTestCase(ResourceTestCase):
    '''
        All the common functionality needed for creating our
        API test cases.
    '''
    def setUp(self):
        ResourceTestCase.setUp(self)
        self.client = self.api_client

    def get_full_uri(self, resource_name):
        '''
            Given the resource name, return the full uri.
        '''
        api_root = settings.API_ROOT
        api_version = settings.API_VERSION
        return "/{0}/{1}/{2}/".format(api_root, api_version, resource_name)

    def get(self, uri, format, **options):
        '''
            Makes a get call and returns the response.
        '''
        return self.client.get(uri, format)

    def get_json(self, uri, apply_assetions):
        '''
            Json specific GET implementation.
        '''
        response = self.get(uri, format="json")

        if apply_assetions:
            # Asset API returns 200 OK.
            self.assertHttpOK(response)
            self.assertValidJSONResponse(response)

    def get_xml(self, uri, apply_assetions):
        '''
            Json specific GET implementation.
        '''
        response = self.get(uri, format="xml")
        if apply_assetions:
            # Asset API returns 200 OK.
            self.assertHttpOK(response)
            self.assertValidXMLResponse(response)


class UserResourceTest(BaseTestCase):
    '''
        Tests users API.
    '''
    def setUp(self):
        BaseTestCase.setUp(self)
        self.resource_name = "users"

    def test_get_json(self):
        '''
            Tests - /api/v1/users/?format=json
        '''
        uri = self.get_full_uri(self.resource_name)
        self.get_json(uri, apply_assetions=True)

    def test_get_xml(self):
        '''
            Tests - /api/v1/users/?format=xml
        '''
        uri = self.get_full_uri(self.resource_name)
        self.get_xml(uri, apply_assetions=True)


class MediaResourceTest(BaseTestCase):
    '''
        Tests medias API.
    '''
    def setUp(self):
        BaseTestCase.setUp(self)
        self.resource_name = "medias"

    def test_get_json(self):
        '''
            Tests - /api/v1/medias/?format=json
        '''
        uri = self.get_full_uri(self.resource_name)
        self.get_json(uri, apply_assetions=True)

    def test_get_xml(self):
        '''
            Tests - /api/v1/medias/?format=xml
        '''
        uri = self.get_full_uri(self.resource_name)
        self.get_xml(uri, apply_assetions=True)


class TweetResourceTest(BaseTestCase):
    '''
        Tests medias API.
    '''
    def setUp(self):
        BaseTestCase.setUp(self)
        self.resource_name = "tweets"

    def test_get_json(self):
        '''
            Tests - /api/v1/tweets/?format=json
        '''
        uri = self.get_full_uri(self.resource_name)
        self.get_json(uri, apply_assetions=True)

    def test_get_xml(self):
        '''
            Tests - /api/v1/tweets/?format=xml
        '''
        uri = self.get_full_uri(self.resource_name)
        self.get_xml(uri, apply_assetions=True)
