from .ressource import Collection, Model


class Attribute(Model):
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

    def drop(self):
        return self.client.api.cl_drop_attribute(self.api_name)


class AttributeCollection(Collection):
    model = Attribute

    def __init__(self, client=None, corpus=None):
        super().__init__(client=client)
        self.corpus = corpus

    def _get(self, attribute_name):
        api_name = f'{self.corpus.api_name}.{attribute_name}'
        return {
            'api_name': api_name,
            'name': attribute_name,
            'size': self.client.api.cl_attribute_size(api_name)
        }

    def get(self, attribute_name):
        return self.prepare_model(self._get(attribute_name))

    def list(self):
        raise NotImplementedError


class AlignmentAttribute(Attribute):
    def cpos_by_ids(self, id_list):
        return self.client.api.cl_alg2cpos(self.api_name, id_list)

    def ids_by_cpos(self, cpos_list):
        return self.client.api.cl_cpos2alg(self.api_name, cpos_list)


class AlignmentAttributeCollection(AttributeCollection):
    model = AlignmentAttribute

    def list(self):
        return [self.prepare_model(self._get(x)) for x
                in self.client.api.corpus_alignment_attributes(self.corpus.api_name)]  # noqa


class PositionalAttribute(Attribute):
    @property
    def lexicon_size(self):
        return self.attrs.get('lexicon_size')

    def cpos_by_id(self, id):
        return self.client.api.cl_id2cpos(self.api_name, id)

    def cpos_by_ids(self, id_list):
        return self.client.api.cl_idlist2cpos(self.api_name, id_list)

    def freqs_by_ids(self, id_list):
        return self.client.api.cl_id2freq(self.api_name, id_list)

    def ids_by_cpos(self, cpos_list):
        return self.client.api.cl_cpos2id(self.api_name, cpos_list)

    def ids_by_regex(self, regex):
        return self.client.api.cl_regex2id(self.api_name, regex)

    def ids_by_values(self, value_list):
        return self.client.api.cl_str2id(self.api_name, value_list)

    def values_by_cpos(self, cpos_list):
        return self.client.api.cl_cpos2str(self.api_name, cpos_list)

    def values_by_ids(self, id_list):
        return self.client.api.cl_id2str(self.api_name, id_list)


class PositionalAttributeCollection(AttributeCollection):
    model = PositionalAttribute

    def _get(self, positional_attribute_name):
        attrs = super()._get(positional_attribute_name)
        attrs['lexicon_size'] = self.client.api.cl_lexicon_size(attrs['api_name'])  # noqa
        return attrs

    def list(self):
        return [self.prepare_model(self._get(x)) for x
                in self.client.api.corpus_positional_attributes(self.corpus.api_name)]  # noqa


class StructuralAttribute(Attribute):
    @property
    def has_values(self):
        return self.attrs.get('has_values')

    def cpos_by_id(self, id):
        return self.client.api.cl_struc2cpos(self.api_name, id)

    def ids_by_cpos(self, cpos_list):
        return self.client.api.cl_cpos2struc(self.api_name, cpos_list)

    def lbound_by_cpos(self, cpos_list):
        return self.client.api.cl_cpos2lbound(self.api_name, cpos_list)

    def rbound_by_cpos(self, cpos_list):
        return self.client.api.cl_cpos2rbound(self.api_name, cpos_list)

    def values_by_ids(self, id_list):
        return self.client.api.cl_struc2str(self.api_name, id_list)


class StructuralAttributeCollection(AttributeCollection):
    model = StructuralAttribute

    def _get(self, structural_attribute_name):
        attrs = super()._get(structural_attribute_name)
        attrs['has_values'] = self.client.api.corpus_structural_attribute_has_values(attrs['api_name'])  # noqa
        return attrs

    def list(self, filters={}):
        structural_attributes = [
            self.prepare_model(self._get(x)) for x
            in self.client.api.corpus_structural_attributes(self.corpus.api_name)  # noqa
        ]
        for k, v in filters.items():
            if k == 'part_of':
                structural_attributes = [x for x in structural_attributes
                                         if x.name.startswith(f'{v.name}_')]
        return structural_attributes
