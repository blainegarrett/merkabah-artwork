"""
Config for artwork module. Provides endpoint mappings
"""

from plugins.artwork.services import ArtworkServices

# Venues api endpoints
service_url_prefix = 'artworks'
service_class = ArtworkServices