from typing import Dict, List, Tuple, Type, TYPE_CHECKING
if TYPE_CHECKING:
    from ..client import CQiClient
    from ..status import StatusOk
    from .corpora import Corpus
from .resource import Collection, Model


class Attribute(Model):
    @property
    def api_name(self) -> str:
        return self.attrs['api_name']

    @property
    def name(self) -> str:
        return self.attrs['name']

    @property
    def size(self) -> int:
        return self.attrs['size']

    def drop(self) -> 'StatusOk':
        ''' unload attribute from memory '''
        return self.client.api.cl_drop_attribute(self.api_name)


class AttributeCollection(Collection):
    model: Type[Attribute] = Attribute

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
    def cpos_by_id(self, id: int) -> Tuple[int, int, int, int]:
        ''' returns (src_start, src_end, target_start, target_end) '''
        return self.client.api.cl_alg2cpos(self.api_name, id)

    def ids_by_cpos(self, cpos_list: List[int]) -> List[int]:
        ''' returns -1 for every corpus position not inside an alignment '''
        return self.client.api.cl_cpos2alg(self.api_name, cpos_list)


class AlignmentAttributeCollection(AttributeCollection):
    model: Type[AlignmentAttribute] = AlignmentAttribute

    def list(self) -> List[AlignmentAttribute]:
        return [
            self.get(x) for x in
            self.client.api.corpus_alignment_attributes(self.corpus.api_name)
        ]


class PositionalAttribute(Attribute):
    @property
    def lexicon_size(self) -> int:
        return self.attrs['lexicon_size']

    def cpos_by_id(self, id: int) -> List[int]:
        ''' returns all corpus positions where the given token occurs '''
        return self.client.api.cl_id2cpos(self.api_name, id)

    def cpos_by_ids(self, id_list: List[int]) -> List[int]:
        '''
        returns all corpus positions where one of the tokens in <id_list>
        occurs; the returned list is sorted as a whole, not per token id
        '''
        return self.client.api.cl_idlist2cpos(self.api_name, id_list)

    def freqs_by_ids(self, id_list: List[int]) -> List[int]:
        ''' returns 0 for every ID in <id_list> that is out of range '''
        return self.client.api.cl_id2freq(self.api_name, id_list)

    def ids_by_cpos(self, cpos_list: List[int]) -> List[int]:
        '''
        returns -1 for every corpus position in <cpos_list> that is out of
        range
        '''
        return self.client.api.cl_cpos2id(self.api_name, cpos_list)

    def ids_by_regex(self, regex: str) -> List[int]:
        '''
        returns lexicon IDs of all tokens that match <regex>; the returned
        list may be empty (size 0);
        '''
        return self.client.api.cl_regex2id(self.api_name, regex)

    def ids_by_values(self, value_list: List[str]) -> List[int]:
        '''
        returns -1 for every string in <value_list> that is not found in the
        lexicon
        '''
        return self.client.api.cl_str2id(self.api_name, value_list)

    def values_by_cpos(self, cpos_list: List[int]) -> List[str]:
        '''
        returns "" for every corpus position in <cpos_list> that is out of
        range
        '''
        return self.client.api.cl_cpos2str(self.api_name, cpos_list)

    def values_by_ids(self, id_list: List[int]) -> List[str]:
        ''' returns "" for every ID in <id_list> that is out of range '''
        return self.client.api.cl_id2str(self.api_name, id_list)


class PositionalAttributeCollection(AttributeCollection):
    model: Type[PositionalAttribute] = PositionalAttribute

    def _get(self, positional_attribute_name: str) -> Dict:
        attrs = super()._get(positional_attribute_name)
        attrs['lexicon_size'] = self.client.api.cl_lexicon_size(attrs['api_name'])
        return attrs

    def list(self) -> List[PositionalAttribute]:
        return [
            self.get(x) for x in
            self.client.api.corpus_positional_attributes(self.corpus.api_name)
        ]


class StructuralAttribute(Attribute):
    @property
    def has_values(self) -> bool:
        return self.attrs['has_values']

    def cpos_by_id(self, id: int) -> Tuple[int, int]:
        '''
        returns start and end corpus positions of structure region with id
        <id>
        '''
        return self.client.api.cl_struc2cpos(self.api_name, id)

    def ids_by_cpos(self, cpos_list: List[int]) -> List[int]:
        '''
        returns -1 for every corpus position not inside a structure region
        '''
        return self.client.api.cl_cpos2struc(self.api_name, cpos_list)

    def lbound_by_cpos(self, cpos_list: List[int]) -> List[int]:
        '''
        returns left boundary of s-attribute region enclosing cpos, -1 if not
        in region
        '''
        return self.client.api.cl_cpos2lbound(self.api_name, cpos_list)

    def rbound_by_cpos(self, cpos_list: List[int]) -> List[int]:
        '''
        returns right boundary of s-attribute region enclosing cpos, -1 if not
        in region
        '''
        return self.client.api.cl_cpos2rbound(self.api_name, cpos_list)

    def values_by_ids(self, id_list: List[int]) -> List[str]:
        '''
        returns annotated string values of structure regions in <id_list>; ""
        if out of range

        check has_values property first
        '''
        return self.client.api.cl_struc2str(self.api_name, id_list)


class StructuralAttributeCollection(AttributeCollection):
    model: Type[StructuralAttribute] = StructuralAttribute

    def _get(self, structural_attribute_name: str) -> Dict:
        attrs = super()._get(structural_attribute_name)
        attrs['has_values'] = self.client.api.corpus_structural_attribute_has_values(attrs['api_name'])
        return attrs

    def list(self, filters: Dict = {}) -> List[StructuralAttribute]:
        structural_attributes = [
            self.get(x) for x in
            self.client.api.corpus_structural_attributes(self.corpus.api_name)
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
