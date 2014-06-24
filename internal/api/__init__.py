# TODO: Move all of this into internal.api.*

import artwork
import images
import series

from merkabah.core.files.api.cloudstorage import Cloudstorage
from settings import DEFAULT_GS_BUCKET_NAME

def create_upload_url(callback_url=None):
    """
    Create an upload url
    """
    # TODO: Move this to merkabah core?

    fs = Cloudstorage(DEFAULT_GS_BUCKET_NAME)

    if not callback_url:
        raise Exception('Invalid Arguments')

    return fs.create_upload_url(callback_url)