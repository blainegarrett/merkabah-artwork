from merkabah.core import forms as merkabah_forms
from django import forms

from .internal import api

class ImageUploadForm(merkabah_forms.MerkabahBaseForm):
    """
    Form for uploading a file to the images Library
    """

    title = forms.CharField(max_length=50)
    the_file = forms.FileField()


class ArtworkForm(merkabah_forms.MerkabahBaseForm):
    slug = forms.CharField(label='Slug', max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Slug'}))
    title = forms.CharField(label='Title', max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Title'}))

    content = forms.CharField(label='Content', required=False, widget=forms.Textarea(attrs={'placeholder': 'Content', 'class': 'ckeditor'}))

    height = forms.IntegerField(label='Height', required=False, widget=forms.TextInput(attrs={'placeholder': 'Height (inches)'}))
    width = forms.IntegerField(label='Width', required=False, widget=forms.TextInput(attrs={'placeholder': 'Width (inches)'}))
    year = forms.IntegerField(label='Year', required=False, widget=forms.TextInput(attrs={'placeholder': 'Year'}))
    price = forms.IntegerField(label='Price', required=False, widget=forms.TextInput(attrs={'placeholder': 'Price'}))
    sale = forms.BooleanField(required=False)


    series = forms.MultipleChoiceField(label='Series', required=False, choices=[])
    attached_media = forms.MultipleChoiceField(label='Attached Media', required=False, choices=[])
    primary_media_image = forms.ChoiceField(label='Primary Image', required=False, choices=[])

    def __init__(self, *args, **kwargs):
        super(ArtworkForm, self).__init__(*args, **kwargs)
        
        # Populate series
        series_choices = []
        series_entities = api.series.get_series_list() # TODO: Convert to api method
        for series_entity in series_entities:
            series_choices.append((series_entity.key.urlsafe(), series_entity.title))

        self.fields['series'].choices = series_choices

        # Populate images
        media_choices = [('', '--No Images --')]
        image_entities = api.images.get_images() # TODO: Convert to api method
        for image_entity in image_entities:
            media_choices.append((image_entity.key.urlsafe(), image_entity.filename))

        self.fields['attached_media'].choices = media_choices
        
        # Primary Image
        self.fields['primary_media_image'].choices = media_choices

        return

        # Primary Image
        media_choices = [('', 'None Selected')]
        media_entities = blog_models.BlogMedia.query().fetch(1000) # TODO: Convert to api method
        for media_entity in media_entities:
            media_choices.append((media_entity.key.urlsafe(), media_entity.filename))

        self.fields['primary_media_image'].choices = media_choices

        # Categories
        categories_choices = []
        category_entities = blog_models.BlogCategory.query().fetch(1000)
        for category_entity in category_entities:
            categories_choices.append((category_entity.key.urlsafe(), category_entity.name))

        self.fields['categories'].choices = categories_choices


class ArtworkSeriesForm(merkabah_forms.MerkabahBaseForm):
    """
    Form for Creatuing and Editing a Series
    """

    title = forms.CharField(label='Title', max_length=100, required=True)
    slug = forms.CharField(label='Slug', max_length=100, required=True)


class BlogMediaForm(merkabah_forms.MerkabahBaseForm):
    image_file = forms.FileField(required=False)
    is_upload = forms.CharField(required=True)
