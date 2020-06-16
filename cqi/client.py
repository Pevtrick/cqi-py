from .api import APIClient
from .models.corpora import CorpusCollection
import math


class CQiClient:
    """
    A client for communicating with a CQi server.

    Example:
    >>> import cqi
    >>> client = cqi.CQiClient('127.0.0.1')
    >>> client.connect()
    258  # CQI_STATUS_CONNECT_OK
    >>> client.ping()
    260  # CQI_STATUS_PING_OK
    >>> client.disconnect()
    259  # CQI_STATUS_BYE_OK

    Attributes:
    api (APIClient): An API client pointing to the specified CQP server.
    """

    def __init__(self, host, port=4877, timeout=math.inf):
        """
        CQiClient constructor

        Args:
        host (str): URL to the CQP server. For example,
            ``cqpserver.localhost`` or ``127.0.0.1``.
        port (int): Port the CQP server listens on. Default: ``4877``
        timeout (int): Time to wait for bytes from the server. If the timeout
            is exceeded, an exception is raised. Default: ``math.inf``
        """
        self.api = APIClient(host, port=port, timeout=timeout)

    def connect(self, username='anonymous', password=''):
        status = self.api.ctrl_connect(username, password)
        return status

    def disconnect(self):
        return self.api.ctrl_bye()

    def ping(self):
        return self.api.ctrl_ping()

    @property
    def corpora(self):
        return CorpusCollection(client=self)
