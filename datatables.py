from merkabah.core import datatable as merkabah_datatable
from django.core import urlresolvers


# Artwork Image Datatables
class ArtworkMediaThumbnailColumn(merkabah_datatable.DatatableColumn):
    """
    """

    def render_content(self, obj, context):
        """
        """

        img_url = obj.get_url()

        output = '<a href="%s"><img class="thumbnail" src="%s" style="max-width:300px;max-height:200px;" alt="Placeholder Image" /></a>' % (img_url, img_url)
        return output


class ArtworkImageGroupActions(object):
    """
    """

    def render_content(self, context):
        link = urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'images_create'))
        return '<a href="%s" class="btn-primary btn">Create</a>' % link


class ArtworkImageGrid(merkabah_datatable.Datatable):
    thumb = ArtworkMediaThumbnailColumn()
    filename = merkabah_datatable.DatatableColumn()
    blob_key = merkabah_datatable.DatatableColumn()
    gcs_filename = merkabah_datatable.DatatableColumn()
    gcs_thumbnail_filename = merkabah_datatable.DatatableColumn()
    gcs_sized_filename = merkabah_datatable.DatatableColumn()
    content_type = merkabah_datatable.DatatableColumn()
    size = merkabah_datatable.DatatableColumn()
    group_actions = ArtworkImageGroupActions()
    column_order = ['thumb', 'filename', 'blob_key', 'gcs_filename', 'content_type', 'size']


# Series Datatables
class ArtworkSeriesActions(object):
    """
    """

    def render_content(self, context):
        link = urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'create_series'))
        output = '<a href="%s" class="btn-primary btn">Create</a>&nbsp;&nbsp;&nbsp;' % link
        return output


class ArtworkSeriesActionColumn(merkabah_datatable.DatatableColumn):
    """
    """

    def render_content(self, obj, context):

        link = urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'edit_series'))
        link = '%s?series_key=%s' % (link, obj.key.urlsafe())
        output = '<a href="%s" class="btn btn-default">Edit</a>' % link

        link = urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'delete_series'))
        link = '%s?series_key=%s' % (link, obj.key.urlsafe())
        output += '<a href="%s" class="btn btn-default">Delete</a>' % link
        return output


class ArtworkSeriesGrid(merkabah_datatable.Datatable):
    # Column Definitions
    title = merkabah_datatable.DatatableColumn()
    slug = merkabah_datatable.DatatableColumn()
    actions = ArtworkSeriesActionColumn()

    column_order = ['title', 'slug', 'actions']

    group_actions = ArtworkSeriesActions()

    def get_row_identifier(self, obj):
        return obj.key.urlsafe()
