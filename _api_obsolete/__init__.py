# TODO: Move all of this into internal.api.*
'''
from google.appengine.ext import ndb

from merkabah.core.files.api.cloudstorage import Cloudstorage
from settings import DEFAULT_GS_BUCKET_NAME

from gallery.models import ArtworkSeries, Artwork, ArtworkMedia

# Artwork
def get_artwork(cursor=None):
    return Artwork.query().fetch(1000)



def create_upload_url(callback_url=None):
    """
    """
    raise Exception('DEPRECATED - Moved to internal.api DELETE ME!')

    fs = Cloudstorage(DEFAULT_GS_BUCKET_NAME)

    if not callback_url:
        raise Exception('Invalid Arguments')

    return fs.create_upload_url(callback_url)


def get_images():
    # TODO: Paginate this, etc
    entities = ArtworkMedia.query().order(-ArtworkMedia.gcs_filename).fetch(1000)

    return entities



def get_series_key_by_keystr(series_keystr):
    # TODO: Validate Kind, etc
    series_key = ndb.Key(urlsafe=series_keystr)
    return series_key
'''