from .api import APIClient
from .models.corpora import CorpusCollection
from . import status
import math


class CQiClient:
    '''
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
    '''

    def __init__(
        self,
        host: str,
        port: int = 4877,
        timeout: float = math.inf,
        version: str = '0.1'
    ):
        '''
        CQiClient constructor

        Args:
        host (str): URL to the CQP server. For example,
            ``cqpserver.localhost`` or ``127.0.0.1``.
        port (int): Port the CQP server listens on. Default: ``4877``
        timeout (int): Time to wait for bytes from the server. If the timeout
            is exceeded, an exception is raised. Default: ``math.inf``
        version (str): The version of the CQi protocol to use. Default: ``0.1``
        '''
        self.api: APIClient = APIClient(
            host,
            port=port,
            timeout=timeout,
            version=version
        )

    @property
    def corpora(self) -> CorpusCollection:
        return CorpusCollection(client=self)

    def bye(self) -> status.StatusByeOk:
        return self.api.ctrl_bye()

    def connect(
        self,
        username: str = 'anonymous',
        password: str = ''
    ) -> status.StatusConnectOk:
        return self.api.ctrl_connect(username, password)

    def ping(self) -> status.StatusPingOk:
        return self.api.ctrl_ping()

    def user_abort(self):
        self.api.ctrl_user_abort()

    # Method aliases
    disconnect = bye