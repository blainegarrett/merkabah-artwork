from merkabah.core.files.api.cloudstorage import Cloudstorage
#from merkabah.core.oldfiles import rescale
from plugins.artwork.internal.models import ArtworkMedia
from django.core import urlresolvers
import logging
from google.appengine.api import images

from google.appengine.ext import ndb

def get_image_key_by_keystr(keystr):
    err = 'Keystrings must be an instance of base string, recieved: %s' % keystr

    if not keystr or not isinstance(keystr, basestring):
        raise RuntimeError(err)

    return ndb.Key(urlsafe=keystr)

def get_images():
    """
    """

    # TODO: Paginate this, etc
    entities = ArtworkMedia.query().fetch(1000)

    return entities


def rescale(img_data, width, height, halign='middle', valign='middle'):
  """Resize then optionally crop a given image.

  Attributes:
    img_data: The image data
    width: The desired width
    height: The desired height
    halign: Acts like photoshop's 'Canvas Size' function, horizontally
            aligning the crop to left, middle or right
    valign: Verticallly aligns the crop to top, middle or bottom

  """

  image = images.Image(img_data)      

  desired_wh_ratio = float(width) / float(height)
  wh_ratio = float(image.width) / float(image.height)

  if desired_wh_ratio > wh_ratio:
    # resize to width, then crop to height
    image.resize(width=width)
    image.execute_transforms()
    trim_y = (float(image.height - height) / 2) / image.height
    if valign == 'top':
      image.crop(0.0, 0.0, 1.0, 1 - (2 * trim_y))
    elif valign == 'bottom':
      image.crop(0.0, (2 * trim_y), 1.0, 1.0)
    else:
      image.crop(0.0, trim_y, 1.0, 1 - trim_y)
  else:
    # resize to height, then crop to width
    image.resize(height=height)
    image.execute_transforms()
    trim_x = (float(image.width - width) / 2) / image.width
    if halign == 'left':
      image.crop(0.0, 0.0, 1 - (2 * trim_x), 1.0)
    elif halign == 'right':
      image.crop((2 * trim_x), 0.0, 1.0, 1.0)
    else:
      image.crop(trim_x, 0.0, 1 - trim_x, 1.0)

  return image.execute_transforms()


def create_media(slug, img_data):
    
    content_type = 'image/jpeg'
    extension = 'jpg'

    # Store in cloud storage
    fs = Cloudstorage('dim-media') # Change to DefaultBucket

    # Regular Image

    # Note: This WILL Overwrite existing files...
    main_filename = 'artwork/images/%s.%s' % (slug, extension)
    fs.write(main_filename, img_data, content_type)

    # Thumbnail
    file_content = rescale(img_data, 365, 235, halign='middle', valign='middle')
    thumbnail_filename = 'artwork/thumbnail/%s.%s' % (slug, extension)
    logging.debug(thumbnail_filename)
    fs.write(thumbnail_filename, file_content, content_type)

    # Sized Images
    img = images.Image(img_data)
    img.resize(width=1000, height=1000)
    img.im_feeling_lucky()
    file_content = img.execute_transforms(output_encoding=images.JPEG)
    sized_filename = 'artwork/sized/%s.%s' % (slug, extension)
    logging.debug(sized_filename)
    fs.write(sized_filename, file_content, content_type)

    media = ArtworkMedia()
    media.filename = '%s.jpg' % slug
    media.content_type = content_type
    media.gcs_filename = main_filename
    media.gcs_sized_filename = sized_filename
    media.gcs_thumbnail_filename = thumbnail_filename
    media.put()

    return media