from google.appengine.ext import ndb

class ArtworkSeries(ndb.Model):
    slug = ndb.StringProperty()
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    showcase = ndb.BooleanProperty(default=False)
    year = ndb.IntegerProperty()


class ArtworkMedia(ndb.Model):
    filename = ndb.StringProperty()
    blob_key = ndb.BlobKeyProperty()
    gcs_filename = ndb.StringProperty()
    gcs_thumbnail_filename = ndb.StringProperty()
    gcs_sized_filename = ndb.StringProperty()
    content_type = ndb.StringProperty()
    size = ndb.IntegerProperty()

    @property
    def size_in_kb(self):
        return self.size * 1000
    
    def get_thumbnail_url(self):
        return self.get_url('thumb')

    def get_sized_url(self):
        return self.get_url('sized')

    def get_full_url(self):
        return self.get_url('full')

    def get_url(self, version='thumb'):
        from merkabah import is_appspot, get_domain
        import settings

        if is_appspot():
            domain = 'commondatastorage.googleapis.com' #TODO: Make this definable in a setting
        else:
            domain = get_domain()

        bucket = settings.DEFAULT_GS_BUCKET_NAME

        if version == 'thumb':
            path = self.gcs_thumbnail_filename
        if version == 'sized':
            path = self.gcs_sized_filename
        if version == 'full':
            path = self.gcs_filename

        if not is_appspot():
            bucket = "_ah/gcs/%s" % bucket
        url = 'http://%s/%s/%s' % (domain, bucket, path)
        return url

    #@classmethod
    #def _get_kind(cls):
    #    return BLOGMEDIA_KIND # This can be overriden in the plugin.config

class Artwork(ndb.Model):
    title = ndb.StringProperty()
    slug = ndb.StringProperty()
    content = ndb.TextProperty()
    published_date = ndb.DateTimeProperty()
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    modified_date = ndb.DateTimeProperty(auto_now=True)
    series = ndb.KeyProperty(repeated=True, kind=ArtworkSeries)
    primary_media_image = ndb.KeyProperty(kind=ArtworkMedia)
    attached_media = ndb.KeyProperty(repeated=True, kind=ArtworkMedia)
    height = ndb.IntegerProperty()
    width = ndb.IntegerProperty()
    year = ndb.IntegerProperty()

    # Some quicky versions of 
    sale = ndb.BooleanProperty(default=False)
    price = ndb.IntegerProperty(default=0)

    def get_primary_image_url(self):
        return ArtworkMedia.get(self.primary_media_image).filename

    def get_permalink(self):
        dt = self.created_date
        return '/%02d/%02d/%02d/%s' % (dt.year, dt.month, dt.day, self.slug)
    
    def get_series(self):
        return ndb.get_multi(self.series)
