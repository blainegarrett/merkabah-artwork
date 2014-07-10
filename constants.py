"""
Default Artwork Plugin Constants
"""
from datetime import datetime
from settings import plugin_settings
import os

PLUGIN_SLUG = os.path.basename(os.path.dirname(__file__))

POSTS_PER_PAGE = 10
PUBLISHED_DATE_MIN = datetime(1970, 1, 1) # Unix time min

ARTWORKSERIES_KIND = 'ArtworkSeries'
ARTWORKMEDIA_KIND = 'ArtworkMedia'
ARTWORK_KIND = 'Artwork'

try:
    ARTWORK_KIND = plugin_settings[PLUGIN_SLUG]['ARTWORK_KIND']
except KeyError:
    pass

try:
    ARTWORKMEDIA_KIND = plugin_settings[PLUGIN_SLUG]['ARTWORKMEDIA_KIND']
except KeyError:
    pass

try:
    ARTWORKSERIES_KIND = plugin_settings[PLUGIN_SLUG]['ARTWORKSERIES_KIND']
except KeyError:
    pass
