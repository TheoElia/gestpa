from unittest import mock

from django.test import TestCase as DjangoTestCase


class ForceHttpMockTestCase(DjangoTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        def mock_create_conn(address, timeout, *args, **kw):
            raise Exception(f"Unmocked request for URL {address}")

        # monkey patching urllib3 to throw an exception on unmocked requests
        urllib3_patch = mock.patch(
            target="urllib3.util.connection.create_connection",
            new=mock_create_conn,
        )
        urllib3_patch.start()
