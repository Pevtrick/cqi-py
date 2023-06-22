from typing import Dict, List, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from ..client import CQiClient
    from ..status import StatusOk
    from .corpora import Corpus
from .resource import Collection, Model


class Attribute(Model):
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

    def drop(self) -> 'StatusOk':
        return self.client.api.cl_drop_attribute(self.api_name)


class AttributeCollection(Collection):
    model: Attribute = Attribute

    def __init__(self, client: 'CQiClient' = None, corpus: 'Corpus' = None):
        super().__init__(client=client)
        self.corpus: 'Corpus' = corpus

    def _get(self, attribute_name: str) -> Dict:
        api_name: str = f'{self.corpus.api_name}.{attribute_name}'
        return {
            'api_name': api_name,
            'name': attribute_name,
            'size': self.client.api.cl_attribute_size(api_name)
        }

    def get(self, attribute_name: str) -> Attribute:
        return self.prepare_model(self._get(attribute_name))

    def list(self) -> List[Attribute]:
        raise NotImplementedError


class AlignmentAttribute(Attribute):
    def cpos_by_ids(self, id: int) -> Tuple[int, int, int, int]:
        return self.client.api.cl_alg2cpos(self.api_name, id)

    def ids_by_cpos(self, cpos_list: List[int]) -> List[int]:
        return self.client.api.cl_cpos2alg(self.api_name, cpos_list)


class AlignmentAttributeCollection(AttributeCollection):
    model: AlignmentAttribute = AlignmentAttribute

    def list(self) -> List[AlignmentAttribute]:
        return [
            self.prepare_model(self._get(x)) for x
            in self.client.api.corpus_alignment_attributes(self.corpus.api_name)
        ]


class PositionalAttribute(Attribute):
    @property
    def lexicon_size(self) -> int:
        return self.attrs.get('lexicon_size')

    def cpos_by_id(self, id: int) -> List[int]:
        return self.client.api.cl_id2cpos(self.api_name, id)

    def cpos_by_ids(self, id_list: List[int]) -> List[int]:
        return self.client.api.cl_idlist2cpos(self.api_name, id_list)

    def freqs_by_ids(self, id_list: List[int]) -> List[int]:
        return self.client.api.cl_id2freq(self.api_name, id_list)

    def ids_by_cpos(self, cpos_list: List[int]) -> List[int]:
        return self.client.api.cl_cpos2id(self.api_name, cpos_list)

    def ids_by_regex(self, regex: str) -> List[int]:
        return self.client.api.cl_regex2id(self.api_name, regex)

    def ids_by_values(self, value_list: List[str]) -> List[int]:
        return self.client.api.cl_str2id(self.api_name, value_list)

    def values_by_cpos(self, cpos_list: List[int]) -> List[str]:
        return self.client.api.cl_cpos2str(self.api_name, cpos_list)

    def values_by_ids(self, id_list: List[int]) -> List[str]:
        return self.client.api.cl_id2str(self.api_name, id_list)


class PositionalAttributeCollection(AttributeCollection):
    model: PositionalAttribute = PositionalAttribute

    def _get(self, positional_attribute_name: str) -> Dict:
        attrs = super()._get(positional_attribute_name)
        attrs['lexicon_size'] = self.client.api.cl_lexicon_size(attrs['api_name'])
        return attrs

    def list(self) -> List[PositionalAttribute]:
        return [
            self.prepare_model(self._get(x)) for x
            in self.client.api.corpus_positional_attributes(self.corpus.api_name)
        ]


class StructuralAttribute(Attribute):
    @property
    def has_values(self) -> bool:
        return self.attrs.get('has_values')

    def cpos_by_id(self, id: int) -> Tuple[int, int]:
        return self.client.api.cl_struc2cpos(self.api_name, id)

    def ids_by_cpos(self, cpos_list: List[int]) -> List[int]:
        return self.client.api.cl_cpos2struc(self.api_name, cpos_list)

    def lbound_by_cpos(self, cpos_list: List[int]) -> List[int]:
        return self.client.api.cl_cpos2lbound(self.api_name, cpos_list)

    def rbound_by_cpos(self, cpos_list: List[int]) -> List[int]:
        return self.client.api.cl_cpos2rbound(self.api_name, cpos_list)

    def values_by_ids(self, id_list: List[int]) -> List[int]:
        return self.client.api.cl_struc2str(self.api_name, id_list)


class StructuralAttributeCollection(AttributeCollection):
    model: StructuralAttribute = StructuralAttribute

    def _get(self, structural_attribute_name: str) -> Dict:
        attrs = super()._get(structural_attribute_name)
        attrs['has_values'] = self.client.api.corpus_structural_attribute_has_values(attrs['api_name'])
        return attrs

    def list(self, filters: Dict = {}) -> List[StructuralAttribute]:
        structural_attributes = [
            self.prepare_model(self._get(x)) for x
            in self.client.api.corpus_structural_attributes(self.corpus.api_name)
        ]
        for k, v in filters.items():
            if k == 'has_values':
                structural_attributes = [
                    x for x in structural_attributes
                    if x.has_values == v
                ]
            elif k == 'part_of':
                structural_attributes = [
                    x for x in structural_attributes
                    if x.name.startswith(f'{v.name}_')
                ]
        return structural_attributes
