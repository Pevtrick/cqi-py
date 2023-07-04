from typing import Dict, List, Type, TYPE_CHECKING
if TYPE_CHECKING:
    from ..client import CQiClient


class Model:
    '''
    A base class for representing a single object on the server.
    '''

    def __init__(
        self,
        attrs: Dict = None,
        client: 'CQiClient' = None,
        collection: 'Collection' = None
    ):
        #: A client pointing at the server that this object is on.
        self.client: 'CQiClient' = client

        #: The collection that this model is part of.
        self.collection: Collection = collection

        #: The raw representation of this object from the API
        self.attrs: Dict = attrs or {}

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.api_name}>'

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.api_name == other.api_name
        )

    def __hash__(self) -> int:
        return hash(f'{self.__class__.__name__}:{self.api_name}')

    @property
    def api_name(self) -> str:
        raise NotImplementedError

    def reload(self):
        '''
        Load this object from the server again and update ``attrs`` with the
        new data.
        '''
        self.attrs = self.collection.get(self.api_name).attrs


class Collection:
    '''
    A base class for representing all objects of a particular type on the
    server.
    '''

    #: The type of object this collection represents, set by subclasses
    model: Type[Model] = Model

    def __init__(self, client: 'CQiClient' = None):
        #: The client pointing at the server that this collection of objects
        #: is on.
        self.client: 'CQiClient' = client

    def list(self) -> List[Model]:
        raise NotImplementedError

    def get(self) -> Model:
        raise NotImplementedError

    def prepare_model(self, attrs) -> Model:
        '''
        Create a model from a set of attributes.
        '''
        if isinstance(attrs, Model):
            attrs.client = self.client
            attrs.collection = self
            return attrs
        elif isinstance(attrs, dict):
            return self.model(
                attrs=attrs,
                client=self.client,
                collection=self
            )
        else:
            raise Exception(f"Can't create {self.model.__name__} from {attrs}")
