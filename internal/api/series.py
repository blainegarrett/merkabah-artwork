# Internal API Methods for Series
from google.appengine.ext import ndb
from plugins.artwork.internal.models import ArtworkSeries
from plugins.artwork.constants import ARTWORKSERIES_KIND


def get_series_key_by_keystr(keystr):
    """
    Given a urlsafe version of an Album key, get the actual key
    """

    attr_err = 'Keystrings must be an instance of base string, recieved: %s' % keystr
    kind_err = 'Expected urlsafe keystr for kind %s but received keystr for kind %s instead.'

    if not keystr or not isinstance(keystr, basestring):
        raise RuntimeError(attr_err)

    key = ndb.Key(urlsafe=keystr)
    if not key.kind() == ARTWORKSERIES_KIND:
        raise RuntimeError(kind_err % (ARTWORKSERIES_KIND, key.kind()))

    return key


def get_series_key(slug):
    """
    Create a db.Key given a seies slug
    """
    err = 'Series slug must be defined and of of type basestring'

    if not slug or not isinstance(slug, basestring):
        raise RuntimeError(err)

    return ndb.Key(ARTWORKSERIES_KIND, slug)


def get_series_by_slug(slug):
    """
    Given a series slug, fetch the series object
    """

    series_key = get_series_key(slug)
    series = series_key.get()
    return series


def edit_series(series_key, data, operator):
    """
    Edit a series
    """
    # TODO: This should be transactional
    # TODO: If slug changes, we need to update the key

    series = series_key.get()

    if not series:
        raise RuntimeError('Series could not be found by Key')

    for field, value in data.items():
        setattr(series, field, value)

    # Record audit, clear cache, etc
    series.put()

    return series


def delete_series(series_key, operator):
    """
    Delete a series
    """
    #TODO: Find all the artwork with this series and remove the series

    # Prep the file on cloud storage to be deleted
    series = series_key.get()

    if not series:
        raise RuntimeError('Series could not be found by Key')

    series_key.delete()
    return True


def get_series_list():
    """
    """

    # TODO: Paginate this, etc
    entities = ArtworkSeries.query().order(-ArtworkSeries.title).fetch(1000)

    return entities


def create_series(data, operator):
    """
    Create a Series
    """

    slug = data['slug']
    title = data['title']

    key = get_series_key(slug)
    entity = ArtworkSeries(key=key, slug=slug, title=title)
    entity.put()
    return entity
