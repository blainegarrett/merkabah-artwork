"""
Tests Cases for Artwork Plugin API Core methods
"""

from mock import patch
from merkabah.tests import MerkabahPluginTestCaseBase
from plugins.artwork.internal import api


class ArtworkApiCaseBase(MerkabahPluginTestCaseBase):
    """
    Base Test case for Artwork Plugin
    """

    def test_base(self):
        #print 'DURING'
        pass

    def tearDown(self):
        pass


@patch('merkabah.core.files.api.cloudstorage.Cloudstorage.__init__', return_value=None)
@patch('merkabah.core.files.api.cloudstorage.Cloudstorage.create_upload_url')
class GetUploadUrlTests(ArtworkApiCaseBase):
    """
    Tests surrounding get_post_by_slug api call
    """

    def test_base(self, m_fs_get_upload_url, m_fs_init):
        # Prep Mocks
        m_fs_get_upload_url.return_value = 'http://examplecdn.com/upload'

        # Call Test Method
        result = api.create_upload_url('http://examplesite.com/success')

        # Test Results
        m_fs_get_upload_url.assert_called_once_with('http://examplesite.com/success')
        self.assertEqual(result, 'http://examplecdn.com/upload')