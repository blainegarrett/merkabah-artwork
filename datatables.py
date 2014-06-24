from merkabah.core import datatable as merkabah_datatable
from django.core import urlresolvers

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
        output +='<a href="%s" class="btn btn-default">Delete</a>' % link
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