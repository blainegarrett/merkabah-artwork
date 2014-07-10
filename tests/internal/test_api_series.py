"""
Tests Surrounding Artwork Series Api
"""

from mock import Mock, patch

from google.appengine.ext import ndb

from ...tests.internal.test_api import ArtworkApiCaseBase
from ...internal.api import series as api
from ...constants import ARTWORKSERIES_KIND, PLUGIN_SLUG


class SeriesApiCaseBase(ArtworkApiCaseBase):
    """
    Base Test Case for Series Api helpers
    """


class GetSeriesKeyTests(SeriesApiCaseBase):
    """
    Tests surrounding getting series key
    """

    def test_base(self):
        test_slug = 'test'
        result_key = api.get_series_key(test_slug)

        self.assertTrue(isinstance(result_key, ndb.Key))
        self.assertEqual(result_key.kind(), ARTWORKSERIES_KIND)

    def test_errors(self):
        """
        Ensure that passing in None or invalid types triggers errors
        """

        self.assertRaises(RuntimeError, api.get_series_key, None)
        self.assertRaises(RuntimeError, api.get_series_key, '')
        self.assertRaises(RuntimeError, api.get_series_key, {})
        self.assertRaises(RuntimeError, api.get_series_key, 612)

class GetSeriesKeyByKeyStrTests(SeriesApiCaseBase):
    """
    Tests surrounding getting the series key via urlsafe keystr
    """

    @patch('plugins.%s.internal.api.series.ndb' % PLUGIN_SLUG)
    def test_base(self, m_ndb):
        """
        Ensure our keystr helper wrapper calls the ndb.Key constructor correctly
        """

        # Setup Mocks
        m_key = Mock()
        m_key.kind.return_value = ARTWORKSERIES_KIND
        m_key_init = Mock(name='mocked Key class', return_value=m_key)
        m_ndb.Key = m_key_init

        # Run code under test
        result = api.get_series_key_by_keystr('some_url_safe_keystr')

        # Check mocks
        self.assertEqual(result, m_key)
        m_key_init.assert_called_once_with(urlsafe='some_url_safe_keystr')

    def test_invalid_kind(self):
        """
        Ensure urlsafe keys from other Kinds do not work
        """

        bad_keystr = ndb.Key('SomeOtherKind', 612).urlsafe()
        self.assertRaises(RuntimeError, api.get_series_key_by_keystr, bad_keystr)

    def test_errors(self):
        """
        Ensure that passing in None or invalid types triggers errors
        """

        self.assertRaises(RuntimeError, api.get_series_key_by_keystr, None)
        self.assertRaises(RuntimeError, api.get_series_key_by_keystr, '')
        self.assertRaises(RuntimeError, api.get_series_key_by_keystr, 612)


class GetSeriesBySlugTests(SeriesApiCaseBase):
    """
    Tests surrounding getting series slug
    """

    @patch('plugins.%s.internal.api.series.get_series_key' % PLUGIN_SLUG)
    def test_base(self, m_get_series_key):
        # Setup Mocks
        test_slug = 'test'
        mock_key = Mock()
        mock_key.get = Mock(return_value='SeriesEntity') # Mock key.get() call

        m_get_series_key.return_value = mock_key

        # Run code under test
        result = api.get_series_by_slug(test_slug)

        # Check mocks
        m_get_series_key.assert_called_once_with('test')
        mock_key.get.assert_called_once_with()
        self.assertEqual(result, 'SeriesEntity')

    def test_errors(self):
        """
        Ensure that passing in None or invalid types triggers errors
        Note: We may want to eventually catch exception and return None
        """

        self.assertRaises(RuntimeError, api.get_series_by_slug, None)
        self.assertRaises(RuntimeError, api.get_series_by_slug, '')
        self.assertRaises(RuntimeError, api.get_series_by_slug, {})
        self.assertRaises(RuntimeError, api.get_series_by_slug, 612)


class CreateSeriesTests(SeriesApiCaseBase):
    pass


class EditSeriesTests(SeriesApiCaseBase):
    pass


class DeleteSeriesTests(SeriesApiCaseBase):
    pass


class FetchSeriesListTests(SeriesApiCaseBase):
    pass
