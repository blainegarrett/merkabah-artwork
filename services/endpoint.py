"""
"""

from google.appengine.ext import endpoints
from protorpc import messages
from protorpc import remote
from protorpc.message_types import VoidMessage

from .. import api

class Artwork(messages.Message):
    title = messages.StringField(1, required=True)
    description = messages.StringField(2)


class ArtworkCollection(messages.Message):
    items = messages.MessageField(Artwork, 1, repeated=True)
    
    
class UploadUrlResponse(messages.Message):
    url = messages.StringField(1, required=True)

class UploadUrlRequest(messages.Message):
    callback = messages.StringField(1, required=True)


@endpoints.api(name='artworks', version='v1', description='API for Artwork management')
class ArtworkApi(remote.Service):

    @endpoints.method(Artwork, Artwork, name='create_artwork', path='create_artworkxxx', http_method='POST')
    def create_artwork(self, request):
        return request

    def list_artwork(self, request):
        pass

    @endpoints.method(UploadUrlRequest, UploadUrlResponse, name='fishassholes', path='create/get_upload_url', http_method='POST')
    def get_upload_url(self, request):        
        upload_url = api.create_upload_url(callback_url=request.callback)
        return UploadUrlResponse(url=upload_url)

application = endpoints.api_server([ArtworkApi])