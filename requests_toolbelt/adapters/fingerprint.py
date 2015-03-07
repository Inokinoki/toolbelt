# -*- coding: utf-8 -*-
"""
requests_toolbelt.fingerprint_adapter
=====================================

This file contains an implementation of a Transport Adapter that validates
the fingerprints of SSL certificates presented upon connection.
"""
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


class FingerprintAdapter(HTTPAdapter):
    """
    A HTTPS Adapter for Python Requests that verifies certificate fingerprints,
    not just certificate hostnames.

    Example usage:

        >>> import requests
        >>> import ssl
        >>> from requests_toolbelt import FingerprintAdapter
        >>> s = requests.Session()
        >>> s.mount(
        ...     'https://twitter.com',
        ...     FingerprintAdapter(twitter_fingerprint)
        ... )

    The fingerprint should be provided as a hexadecimal string, optionally
    containing colons.
    """

    __attrs__ = HTTPAdapter.__attrs__ + ['fingerprint']

    def __init__(self, fingerprint, **kwargs):
        self.fingerprint = fingerprint

        super(FingerprintAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       assert_fingerprint=self.fingerprint)