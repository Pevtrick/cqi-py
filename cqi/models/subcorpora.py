from .ressource import Collection, Model
from ..api.specification import (CONST_FIELD_KEYWORD, CONST_FIELD_MATCH,
                                 CONST_FIELD_MATCHEND, CONST_FIELD_TARGET)


class Subcorpus(Model):
    id_attribute = 'api_name'

    @property
    def api_name(self):
        return self.attrs.get('api_name')

    @property
    def fields(self):
        return self.attrs.get('fields')

    @property
    def name(self):
        return self.attrs.get('name')

    @property
    def size(self):
        return self.attrs.get('size')

    def drop(self):
        return self.client.api.cqp_drop_subcorpus(self.api_name)

    def dump(self, field, first, last):
        return self.client.api.cqp_dump_subcorpus(
            self.api_name, field, first, last)

    def fdist_1(self, cutoff, field, attribute):
        return self.client.api.cqp_fdist_1(
            self.api_name, cutoff, field, attribute.api_name)

    def fdist_2(self, cutoff, field_1, attribute_1, field_2, attribute_2):
        return self.client.api.cqp_fdist_2(
            self.api_name,
            cutoff,
            field_1,
            attribute_1.api_name,
            field_2,
            attribute_2.api_name
        )


class SubcorpusCollection(Collection):
    model = Subcorpus

    def __init__(self, client=None, corpus=None):
        super().__init__(client=client)
        self.corpus = corpus

    def _get(self, subcorpus_name):
        api_name = f'{self.corpus.api_name}:{subcorpus_name}'
        fields = {}
        if self.client.api.cqp_subcorpus_has_field(api_name, CONST_FIELD_MATCH):  # noqa
            fields['match'] = CONST_FIELD_MATCH
        if self.client.api.cqp_subcorpus_has_field(api_name, CONST_FIELD_MATCHEND):  # noqa
            fields['matchend'] = CONST_FIELD_MATCHEND
        if self.client.api.cqp_subcorpus_has_field(api_name, CONST_FIELD_TARGET):  # noqa
            fields['target'] = CONST_FIELD_TARGET
        if self.client.api.cqp_subcorpus_has_field(api_name, CONST_FIELD_KEYWORD):  # noqa
            fields['keyword'] = CONST_FIELD_KEYWORD
        return {
            'api_name': api_name,
            'fields': fields,
            'name': subcorpus_name,
            'size': self.client.api.cqp_subcorpus_size(api_name)
        }

    def get(self, subcorpus_name):
        return self.prepare_model(self._get(subcorpus_name))

    def list(self):
        return [self.prepare_model(self._get(x)) for x
                in self.client.api.cqp_list_subcorpora(self.corpus.api_name)]
