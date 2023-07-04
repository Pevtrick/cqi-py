from typing import Dict, List, Type, TYPE_CHECKING
if TYPE_CHECKING:
    from ..status import StatusOk
from .attributes import (
    AlignmentAttributeCollection,
    PositionalAttributeCollection,
    StructuralAttributeCollection
)
from .resource import Collection, Model
from .subcorpora import SubcorpusCollection


class Corpus(Model):
    @property
    def api_name(self) -> str:
        return self.attrs['api_name']

    @property
    def name(self) -> str:
        return self.attrs['name']

    @property
    def size(self) -> int:
        return self.attrs['size']

    @property
    def charset(self) -> str:
        return self.attrs['charset']

    @property
    def properties(self) -> List[str]:
        return self.attrs['properties']

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

    def drop(self) -> 'StatusOk':
        ''' try to unload a corpus and all its attributes from memory '''
        return self.client.api.corpus_drop_corpus(self.api_name)

    def query(self, subcorpus_name: str, query: str) -> 'StatusOk':
        ''' <query> must include the ';' character terminating the query. '''
        return self.client.api.cqp_query(self.api_name, subcorpus_name, query)


class CorpusCollection(Collection):
    model: Type[Corpus] = Corpus

    def _get(self, corpus_name: str) -> Dict:
        api_name: str = corpus_name
        p_attr_names: List[str] = self.client.api.corpus_positional_attributes(api_name)
        corpus_size: int = (
            0 if len(p_attr_names) == 0 else
            self.client.api.cl_attribute_size(f'{api_name}.{p_attr_names[0]}')
        )
        return {
            'api_name': api_name,
            'charset': self.client.api.corpus_charset(api_name),
            # 'full_name': self.client.api.corpus_full_name(api_name),
            # 'info': self.client.api.corpus_info(api_name),
            'name': corpus_name,
            'properties': self.client.api.corpus_properties(api_name),
            'size': corpus_size
        }

    def get(self, corpus_name: str) -> Corpus:
        return self.prepare_model(self._get(corpus_name))

    def list(self) -> List[Corpus]:
        return [self.get(x) for x in self.client.api.corpus_list_corpora()]
