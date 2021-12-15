from .attributes import (AlignmentAttributeCollection,
                         PositionalAttributeCollection,
                         StructuralAttributeCollection)
from .ressource import Collection, Model
from .subcorpora import SubcorpusCollection


class Corpus(Model):
    id_attribute = 'api_name'

    @property
    def api_name(self):
        return self.attrs.get('api_name')

    @property
    def name(self):
        return self.attrs.get('name')

    @property
    def size(self):
        return self.attrs.get('size')

    @property
    def charset(self):
        return self.attrs.get('charset')

    @property
    def properties(self):
        return self.attrs.get('properties')

    @property
    def alignment_attributes(self):
        return AlignmentAttributeCollection(client=self.client, corpus=self)

    @property
    def positional_attributes(self):
        return PositionalAttributeCollection(client=self.client, corpus=self)

    @property
    def structural_attributes(self):
        return StructuralAttributeCollection(client=self.client, corpus=self)

    @property
    def subcorpora(self):
        return SubcorpusCollection(client=self.client, corpus=self)

    def drop(self):
        return self.client.api.corpus_drop_corpus(self.api_name)

    def query(self, subcorpus_name, query):
        return self.client.api.cqp_query(self.api_name, subcorpus_name, query)


class CorpusCollection(Collection):
    model = Corpus

    def _get(self, corpus_name):
        api_name = corpus_name
        return {
            'api_name': corpus_name,
            'charset': self.client.api.corpus_charset(api_name),
            # 'full_name' = client.api.corpus_full_name(api_name),
            # 'info': client.api.corpus_info(api_name),
            'name': corpus_name,
            'properties': self.client.api.corpus_properties(api_name),
            'size': self.client.api.cl_attribute_size(f'{api_name}.word')
        }

    def get(self, corpus_name):
        return self.prepare_model(self._get(corpus_name))

    def list(self):
        return [self.prepare_model(self._get(x)) for x
                in self.client.api.corpus_list_coprora()]
