class Model:
    """
    A base class for representing a single object on the server.
    """
    id_attribute = 'Id'

    def __init__(self, attrs=None, client=None, collection=None):
        #: A client pointing at the server that this object is on.
        self.client = client

        #: The collection that this model is part of.
        self.collection = collection

        #: The raw representation of this object from the API
        self.attrs = attrs or {}

    @staticmethod
    def _attrs(client, key):
        raise NotImplementedError

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.id)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self):
        return hash("{}:{}".format(self.__class__.__name__, self.id))

    @property
    def id(self):
        """
        The ID of the object.
        """
        return self.attrs.get(self.id_attribute)

    def reload(self):
        """
        Load this object from the server again and update ``attrs`` with the
        new data.
        """
        new_model = self.collection.get(self.id)
        self.attrs = new_model.attrs


class Collection:
    """
    A base class for representing all objects of a particular type on the
    server.
    """

    #: The type of object this collection represents, set by subclasses
    model = None

    def __init__(self, client=None):
        #: The client pointing at the server that this collection of objects
        #: is on.
        self.client = client

    def list(self):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def prepare_model(self, attrs):
        """
        Create a model from a set of attributes.
        """
        if isinstance(attrs, Model):
            attrs.client = self.client
            attrs.collection = self
            return attrs
        elif isinstance(attrs, dict):
            return self.model(attrs=attrs, client=self.client, collection=self)
        else:
            raise Exception("Can't create {} from {}".format(
                self.model.__name__, attrs))
