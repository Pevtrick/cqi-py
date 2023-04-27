from typing import Dict, List
from .. import status
from .attributes import (
    AlignmentAttributeCollection,
    PositionalAttributeCollection,
    StructuralAttributeCollection
)
from .ressource import Collection, Model
from .subcorpora import SubcorpusCollection


class Corpus(Model):
    id_attribute: str = 'api_name'

    @property
    def api_name(self) -> str:
        return self.attrs.get('api_name')

    @property
    def name(self) -> str:
        return self.attrs.get('name')

    @property
    def size(self) -> int:
        return self.attrs.get('size')

    @property
    def charset(self) -> str:
        return self.attrs.get('charset')

    @property
    def properties(self) -> List[str]:
        return self.attrs.get('properties')

    @property
    def alignment_attributes(self) -> AlignmentAttributeCollection:
        return AlignmentAttributeCollection(client=self.client, corpus=self)

    @property
    def positional_attributes(self) -> PositionalAttributeCollection:
        return PositionalAttributeCollection(client=self.client, corpus=self)

    @property
    def structural_attributes(self) -> StructuralAttributeCollection:
        return StructuralAttributeCollection(client=self.client, corpus=self)

    @property
    def subcorpora(self) -> SubcorpusCollection:
        return SubcorpusCollection(client=self.client, corpus=self)

    def drop(self) -> status.StatusOk:
        return self.client.api.corpus_drop_corpus(self.api_name)

    def query(self, subcorpus_name: str, query: str) -> status.StatusOk:
        return self.client.api.cqp_query(self.api_name, subcorpus_name, query)


class CorpusCollection(Collection):
    model: Corpus = Corpus

    def _get(self, corpus_name: str) -> Dict:
        api_name: str = corpus_name
        return {
            'api_name': corpus_name,
            'charset': self.client.api.corpus_charset(api_name),
            # 'full_name' = client.api.corpus_full_name(api_name),
            # 'info': client.api.corpus_info(api_name),
            'name': corpus_name,
            'properties': self.client.api.corpus_properties(api_name),
            'size': self.client.api.cl_attribute_size(f'{api_name}.word')
        }

    def get(self, corpus_name: str) -> Corpus:
        return self.prepare_model(self._get(corpus_name))

    def list(self) -> List[Corpus]:
        return [
            self.prepare_model(self._get(x)) for x
            in self.client.api.corpus_list_coprora()
        ]
