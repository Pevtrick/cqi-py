from typing import Dict, List, Type, TYPE_CHECKING
if TYPE_CHECKING:
    from ..client import CQiClient
    from ..status import StatusOk
    from .attributes import PositionalAttribute
    from .corpora import Corpus
from ..api.specification import (
    CONST_FIELD_KEYWORD,
    CONST_FIELD_MATCH,
    CONST_FIELD_MATCHEND,
    CONST_FIELD_TARGET
)
from .resource import Collection, Model


class Subcorpus(Model):
    @property
    def api_name(self) -> str:
        return self.attrs['api_name']

    @property
    def fields(self) -> Dict[str, int]:
        return self.attrs['fields']

    @property
    def name(self) -> str:
        return self.attrs['name']

    @property
    def size(self) -> int:
        return self.attrs['size']

    def drop(self) -> 'StatusOk':
        ''' delete a subcorpus from memory '''
        return self.client.api.cqp_drop_subcorpus(self.api_name)

    def dump(self, field: int, first: int, last: int) -> List[int]:
        '''
        Dump the values of <field> for match ranges <first> .. <last> in
        subcorpus. <field> is one of the CQI_CONST_FIELD_* constants.
        '''
        return self.client.api.cqp_dump_subcorpus(
            self.api_name,
            field,
            first,
            last
        )

    def fdist_1(
        self,
        cutoff: int,
        field: int,
        attribute: 'PositionalAttribute'
    ) -> List[int]:
        '''
        frequency distribution of single tokens

        returns <n> (id, frequency) pairs flattened into a list of size 2*<n>

        field is one of
        - CQI_CONST_FIELD_MATCH
        - CQI_CONST_FIELD_TARGET
        - CQI_CONST_FIELD_KEYWORD

        NB: pairs are sorted by frequency desc.
        '''
        return self.client.api.cqp_fdist_1(
            self.api_name,
            cutoff,
            field,
            attribute.api_name
        )

    def fdist_2(
        self,
        cutoff: int,
        field_1: int,
        attribute_1: 'PositionalAttribute',
        field_2: int,
        attribute_2: 'PositionalAttribute'
    ) -> List[int]:
        '''
        frequency distribution of pairs of tokens

        returns <n> (id1, id2, frequency) pairs flattened into a list of size
        3*<n>

        NB: triples are sorted by frequency desc.
        '''
        return self.client.api.cqp_fdist_2(
            self.api_name,
            cutoff,
            field_1,
            attribute_1.api_name,
            field_2,
            attribute_2.api_name
        )


class SubcorpusCollection(Collection):
    model: Type[Subcorpus] = Subcorpus

    def __init__(self, client: 'CQiClient' = None, corpus: 'Corpus' = None):
        super().__init__(client=client)
        self.corpus: 'Corpus' = corpus

    def _get(self, subcorpus_name: str) -> Dict:
        api_name: str = f'{self.corpus.api_name}:{subcorpus_name}'
        fields: Dict[str, int] = {}
        if self.client.api.cqp_subcorpus_has_field(api_name, CONST_FIELD_MATCH):
            fields['match'] = CONST_FIELD_MATCH
        if self.client.api.cqp_subcorpus_has_field(api_name, CONST_FIELD_MATCHEND):
            fields['matchend'] = CONST_FIELD_MATCHEND
        if self.client.api.cqp_subcorpus_has_field(api_name, CONST_FIELD_TARGET):
            fields['target'] = CONST_FIELD_TARGET
        if self.client.api.cqp_subcorpus_has_field(api_name, CONST_FIELD_KEYWORD):
            fields['keyword'] = CONST_FIELD_KEYWORD
        return {
            'api_name': api_name,
            'fields': fields,
            'name': subcorpus_name,
            'size': self.client.api.cqp_subcorpus_size(api_name)
        }

    def get(self, subcorpus_name: str) -> Subcorpus:
        return self.prepare_model(self._get(subcorpus_name))

    def list(self) -> List[Subcorpus]:
        return [
            self.get(x) for x in
            self.client.api.cqp_list_subcorpora(self.corpus.api_name)
        ]
