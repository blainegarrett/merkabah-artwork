from plugins.artwork.internal.models import Artwork
from django.core import urlresolvers
import logging

from google.appengine.ext import ndb
from plugins.artwork.internal.api import series as series_api
from plugins.artwork.internal.api import images as images_api

def get_artwork_key_by_keystr(keystr):
    err = 'Keystrings must be an instance of base string, recieved: %s' % keystr

    if not keystr or not isinstance(keystr, basestring):
        raise RuntimeError(err)

    return ndb.Key(urlsafe=keystr)
    
def get_artwork_key(slug):
    """
    Create a db.Key given a seies slug
    """

    # TODO: Get Kind name off plugin def

    err = 'Artwork slug must be defined and of of type basestring'

    if not slug or not isinstance(slug, basestring):
        raise RuntimeError(err)

    return ndb.Key('Artwork', slug)

def get_artwork():
    """
    Return a list of artwork
    """

    # TODO: Paginate this, etc
    entities = Artwork.query().fetch(1000)

    return entities


def get_artwork_by_series(series_key):
    """
    TODO: Paginate this, etc
    """

    return Artwork.query(Artwork.series == series_key)

def get_featured_artwork():
    return Artwork.query()


def create_artwork(data, operator):
    slug = data['slug']

    key = get_artwork_key(slug)

    #raise Exception(data)

    # Process Series
    series_keystrs = data.get('series', '')
    series_keys = []
    if series_keystrs:
        for keystr in series_keystrs:
            series_key = series_api.get_series_key_by_keystr(keystr)
            if series_key:
                series_keys.append(series_key)

    data['series'] = series_keys

    # Process Artwork Selection
    image_keystrs = data.get('attached_media', '')
    image_keys = []
    if image_keystrs:
        for keystr in image_keystrs:
            image_key = images_api.get_image_key_by_keystr(keystr)
            if image_key:
                image_keys.append(image_key)

    data['attached_media'] = image_keys

    # Primary Image
    primary_image_key = None
    primary_image_keystr = data.get('primary_media_image', '')
    if primary_image_keystr:
        primary_image_key = images_api.get_image_key_by_keystr(keystr)
    data['primary_media_image'] = primary_image_key

    entity = Artwork(key=key, **data)

    entity.put()
    return entity

def edit_artwork(artwork_key, data, operator):
    artwork = artwork_key.get()

    if not artwork:
        raise RuntimeError('Artwork could not be found by Key')

    # Process Series
    series_keystrs = data.get('series', '')
    series_keys = []
    if series_keystrs:
        for keystr in series_keystrs:
            series_key = series_api.get_series_key_by_keystr(keystr)
            if series_key:
                series_keys.append(series_key)

    data['series'] = series_keys

    # Process Artwork Selection
    image_keystrs = data.get('attached_media', '')
    image_keys = []
    if image_keystrs:
        for keystr in image_keystrs:
            image_key = images_api.get_image_key_by_keystr(keystr)
            if image_key:
                image_keys.append(image_key)

    data['attached_media'] = image_keys

    # Primary Image
    primary_image_key = None
    primary_image_keystr = data.get('primary_media_image', '')
    if primary_image_keystr:
        primary_image_key = images_api.get_image_key_by_keystr(keystr)
    data['primary_media_image'] = primary_image_key

    for field, value in data.items():
        setattr(artwork, field, value)

    artwork.put()
    return artwork
  