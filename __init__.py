"""
Artwork Plugin
"""

from plugins.artwork.internal import api
from merkabah.core.controllers import TemplateResponse
from merkabah.core import datatable as merkabah_datatable
from django.core import urlresolvers

from settings import DEFAULT_GS_BUCKET_NAME
from forms import ImageUploadForm, ArtworkSeriesForm
from merkabah.core.controllers import FormResponse
from django.http import HttpResponseRedirect
import logging

from datatables import ArtworkSeriesGrid


class ArtworkPlugin(object):
    """
    """

    name = 'Artwork'
    entity_nice_name = 'art'
    entity_plural_name = 'art'

    def process_index(self, request, context, *args, **kwargs):
        """
        Driver switchboard logic
        """

        entities = api.artwork.get_artwork()
        context['grid'] = ArtworkGrid(entities, request, context)
        return TemplateResponse('admin/plugin/index.html', context)

    # Artwork - Not started
    def process_create(self, request, context, *args, **kwargs):
        """
        Create a piece of artwork
        """

        context['form'] = 'main'
        return TemplateResponse(self, 'admin/plugin/form.html', context)

    # Artwork Images
    def process_images(self, request, context, *args, **kwargs):
        """
        Display a list of Images
        """

        entities = api.images.get_images()
        context['grid'] = ArtworkImageGrid(entities, request, context)

        return TemplateResponse('admin/plugin/index.html', context)

    def process_images_create(self, request, context, *args, **kwargs):
        """
        Upload a new image to the Artwork Gallery
        """

        from merkabah.core.files.api.cloudstorage import Cloudstorage
        from google.appengine.ext import blobstore
        from plugins.artwork.internal.api.images import create_media

        # Get the file upload url

        fs = Cloudstorage(DEFAULT_GS_BUCKET_NAME)

        form = ImageUploadForm()

        context['form'] = form
        has_files = fs.get_uploads(request, 'the_file', True)


        if has_files:
            file_info = has_files[0]

            original_filename = file_info.filename
            content_type = file_info.content_type
            size = file_info.size
            gs_object_name = file_info.gs_object_name # Using this we could urlfetch, but the file isn't public...
            blob_key = blobstore.create_gs_key(gs_object_name)
            logging.warning(blob_key)
            data =  fs.read(gs_object_name.replace('/gs', ''))
            
            slug = original_filename.split('.')[0] # I dislike this..

            media = create_media(slug, data)

            # What we want to do now is create a copy of the file with our own info

            dest_filename = '%s' % original_filename

            new_gcs_filename = fs.write(dest_filename, data, content_type)
            logging.warning(new_gcs_filename)

            # Finally delete the tmp file
            data =  fs.delete(gs_object_name.replace('/gs', ''))

            return HttpResponseRedirect(urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'images')))

        upload_url = fs.create_upload_url('/madmin/plugin/artwork/images_create/')

        return FormResponse(form, id='images_create_form', title="Upload a file", target_url=upload_url, target_action='images_create', is_upload=True)
    
    def process_series(self, request, context, *args, **kwargs):
        """
        Method to Display a set of series
        """

        entities = api.series.get_series_list()
        context['grid'] = ArtworkSeriesGrid(entities, request, context)
        return TemplateResponse('admin/plugin/index.html', context)

    def process_edit_series(self, request, context, *args, **kwargs):
        """
        Handler for editing a series
        """
        series_keystr = request.REQUEST['series_key']

        if not series_keystr:
            raise RuntimeError('No argument post_key provided.')

        series_key = api.series.get_series_key_by_keystr(series_keystr)
        series = series_key.get() # TODO: Make into api method

        initial_data = {
            'slug': series.slug,
            'title': series.title
        }

        form = ArtworkSeriesForm(initial=initial_data)

        context['form'] = form

        if request.POST:
            context['form'] = ArtworkSeriesForm(request.POST)
            if context['form'].is_valid():
                form_data = context['form'].cleaned_data
                series = api.series.edit_series(series_key, form_data, operator=None) #TODO: Add operator
                return HttpResponseRedirect(urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'series')))

        target_url = "%s?series_key=%s" % (urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'edit_series')), series_key.urlsafe())
        return FormResponse(form, id='series_edit_form', title="Edit", target_url=target_url, target_action='edit_series')

    def process_create_series(self, request, context, *args, **kwargs):
        """
        Handler for creating a series
        """
        form = ArtworkSeriesForm()

        context['form'] = form

        if request.POST:
            context['form'] = ArtworkSeriesForm(request.POST)
            if context['form'].is_valid():
                form_data = context['form'].cleaned_data
                series = api.series.create_series(form_data, operator=None) #TODO: Add operator
                return HttpResponseRedirect(urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'series')))

        return FormResponse(form, id='series_create_form', title="Create", target_url='/madmin/plugin/artwork/create_series/', target_action='create_series')

    def process_delete_series(self, request, context, *args, **kwargs):
        """
        Handler for deleting a series
        """
        # TODO: Need to handle confirmation

        series_keystr = request.REQUEST['series_key']

        if not series_keystr:
            raise RuntimeError('No argument media_key provided.')

        series_key = api.series.get_series_key_by_keystr(series_keystr)

        # Call api to delete series, etc
        api.series.delete_series(series_key, operator=None)

        return HttpResponseRedirect(urlresolvers.reverse('admin_plugin_action', args=(context['plugin_slug'], 'series')))



class ArtworkActionColumn(merkabah_datatable.DatatableColumn):
    def render_content(self, obj):
        link = urlresolvers.reverse('merkabah_admin_blog_post_edit', args=(obj.key.urlsafe(),))
        output = '<a href="%s" class="button">Edit</a>' % link

        link = obj.get_permalink()
        output += '<a href="%s" class="button">View</a>' % link

        return output


class BlogCategoryActionColumn(merkabah_datatable.DatatableColumn):
    def render_content(self, obj):
        link = urlresolvers.reverse('merkabah_admin_blog_category_edit', args=(obj.key.urlsafe(),))
        return '<a href="%s" class="button">Edit</a>' % link


class ArtworkGrid(merkabah_datatable.Datatable):
    # Column Definitions
    title = merkabah_datatable.DatatableColumn()
    slug = merkabah_datatable.DatatableColumn()
    created_date = merkabah_datatable.DatatableColumn()
    published_date = merkabah_datatable.DatatableColumn()
    actions = ArtworkActionColumn()
    column_order = ['title' , 'slug', 'published_date', 'created_date', 'actions']


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
    column_order = ['thumb', 'filename' , 'blob_key', 'gcs_filename', 'content_type', 'size']


# Register Plugin
pluginClass = ArtworkPlugin
