from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .status import StatusByeOk, StatusConnectOk, StatusPingOk
from .api import APIClient
from .models.corpora import CorpusCollection



class CQiClient:
    '''
    A client for communicating with a CQi server.

    Example:
    >>> import cqi
    >>> client = cqi.CQiClient('127.0.0.1')
    >>> client.connect('username', 'password')
    <class 'cqi.status.StatusConnectOk'>
    >>> client.ping()
    <class 'cqi.status.StatusPingOk'>

    Args:
    host (str): URL to the CQP server.
        For example ``cqpserver.localhost`` or ``127.0.0.1``.
    port (int): Port the CQP server listens on.
        Default: ``4877``
    version (str): The version of the CQi protocol to use.
        Default: ``0.1``
    max_bufsize (int): Maximum number of bytes to receive at once.
        Default: ``4096``
    timeout (float): Default timeout for API calls, in seconds.
        Default: ``60.0``
    '''

    def __init__(self, *args, **kwargs):
        self.api: APIClient = APIClient(*args, **kwargs)

    @property
    def corpora(self) -> CorpusCollection:
        return CorpusCollection(client=self)

    def bye(self) -> 'StatusByeOk':
        return self.api.ctrl_bye()

    def connect(self, username: str, password: str) -> 'StatusConnectOk':
        return self.api.ctrl_connect(username, password)

    def ping(self) -> 'StatusPingOk':
        return self.api.ctrl_ping()

    def user_abort(self):
        self.api.ctrl_user_abort()

    # Method aliases
    disconnect = bye
