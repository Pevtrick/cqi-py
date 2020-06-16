from .ressource import Collection, Model


class Attribute(Model):
    """
    This is a class representing an attribute. Attributes denote the general
    category of information. A specific occurence is identified by an Id.
    """

    id_attribute = 'api_name'

    @staticmethod
    def _attrs(client, corpus, name):
        api_name = '{}.{}'.format(corpus.attrs['api_name'], name)
        return {'api_name': api_name,
                'name': name,
                'size': client.api.cl_attribute_size(api_name)}

    def drop(self):
        return self.client.api.cl_drop_attribute(self.attrs['api_name'])


class AttributeCollection(Collection):
    model = Attribute

    def __init__(self, client=None, corpus=None):
        super(AttributeCollection, self).__init__(client=client)
        self.corpus = corpus

    def get(self, attribute_name):
        return self.prepare_model(self.model._attrs(self.client, self.corpus,
                                                    attribute_name))

    def list(self):
        raise NotImplementedError


class AlignmentAttribute(Attribute):
    def cpos_by_ids(self, id_list):
        return self.client.api.cl_alg2cpos(self.attrs['api_name'], id_list)

    def ids_by_cpos(self, cpos_list):
        return self.client.api.cl_cpos2alg(self.attrs['api_name'], cpos_list)


class AlignmentAttributeCollection(AttributeCollection):
    model = AlignmentAttribute

    def list(self):
        return [self.prepare_model(self.model._attrs(self.client, self.corpus, attr))  # noqa
                for attr in self.client.api.corpus_alignment_attributes(self.corpus.attrs['api_name'])]  # noqa


class PositionalAttribute(Attribute):
    @staticmethod
    def _attrs(client, corpus, name):
        attrs = super(PositionalAttribute, PositionalAttribute)._attrs(client, corpus, name)  # noqa
        attrs['lexicon_size'] = client.api.cl_lexicon_size(attrs['api_name'])
        return attrs

    def cpos_by_id(self, id):
        return self.client.api.cl_id2cpos(self.attrs['api_name'], id)

    def cpos_by_ids(self, id_list):
        return self.client.api.cl_idlist2cpos(self.attrs['api_name'], id_list)

    def freqs_by_ids(self, id_list):
        return self.client.api.cl_id2freq(self.attrs['api_name'], id_list)

    def ids_by_cpos(self, cpos_list):
        return self.client.api.cl_cpos2id(self.attrs['api_name'], cpos_list)

    def ids_by_regex(self, regex):
        return self.client.api.cl_regex2id(self.attrs['api_name'], regex)

    def ids_by_values(self, value_list):
        return self.client.api.cl_str2id(self.attrs['api_name'], value_list)

    def values_by_cpos(self, cpos_list):
        return self.client.api.cl_cpos2str(self.attrs['api_name'], cpos_list)

    def values_by_ids(self, id_list):
        return self.client.api.cl_id2str(self.attrs['api_name'], id_list)


class PositionalAttributeCollection(AttributeCollection):
    model = PositionalAttribute

    def list(self):
        return [self.prepare_model(self.model._attrs(self.client, self.corpus, attr))  # noqa
                for attr in self.client.api.corpus_positional_attributes(self.corpus.attrs['api_name'])]  # noqa


class StructuralAttribute(Attribute):
    @staticmethod
    def _attrs(client, corpus, name):
        attrs = super(StructuralAttribute, StructuralAttribute)._attrs(client, corpus, name)  # noqa
        attrs['has_values'] = client.api.corpus_structural_attribute_has_values(attrs['api_name'])  # noqa
        return attrs

    def cpos_by_id(self, id):
        return self.client.api.cl_struc2cpos(self.attrs['api_name'], id)

    def ids_by_cpos(self, cpos_list):
        return self.client.api.cl_cpos2struc(self.attrs['api_name'], cpos_list)

    def lbound_by_cpos(self, cpos_list):
        return self.client.api.cl_cpos2lbound(self.attrs['api_name'],
                                              cpos_list)

    def rbound_by_cpos(self, cpos_list):
        return self.client.api.cl_cpos2rbound(self.attrs['api_name'],
                                              cpos_list)

    def values_by_ids(self, id_list):
        return self.client.api.cl_struc2str(self.attrs['api_name'], id_list)

    def export(self, first_cpos, last_cpos, context=0, expand_lists=False):
        first_id, last_id = self.ids_by_cpos([first_cpos, last_cpos])
        c = (first_cpos, last_cpos)
        lc = rc = None
        if context == 0:
            cpos_list = list(range(first_cpos, (last_cpos + 1)))
        else:
            lc_lbound = self.cpos_by_id(max(0, (first_id - context)))[0]
            if lc_lbound != first_cpos:
                lc_rbound = max(0, (first_cpos - 1))
                lc = (lc_lbound, lc_rbound)
                cpos_list_lbound = lc_lbound
            else:
                cpos_list_lbound = first_cpos
            rc_rbound = \
                self.cpos_by_id(min((last_id + context),
                                    (self.attrs['size'] - 1)))[1]
            if rc_rbound != last_cpos:
                rc_lbound = min((last_cpos + 1),
                                (self.collection.corpus.attrs['size'] - 1))
                rc = (rc_lbound, rc_rbound)
                cpos_list_rbound = rc_rbound
            else:
                cpos_list_rbound = last_cpos
            cpos_list = list(range(cpos_list_lbound, (cpos_list_rbound + 1)))
        if expand_lists:
            match = {'lc': list(range(lc[0], (lc[1] + 1))),
                     'c': list(range(c[0], (c[1] + 1))),
                     'rc': list(range(rc[0], (rc[1] + 1)))}
        else:
            match = {'lc': lc, 'c': c, 'rc': rc}
        lookups = self.collection.corpus.lookups_by_cpos(cpos_list)
        return {'matches': [match], **lookups}


class StructuralAttributeCollection(AttributeCollection):
    model = StructuralAttribute

    def list(self, filters={}):
        attrs = [self.prepare_model(self.model._attrs(self.client, self.corpus, attr))  # noqa
                 for attr in self.client.api.corpus_structural_attributes(self.corpus.attrs['api_name'])]  # noqa
        for k, v in filters.items():
            if k == 'part_of':
                attrs = list(filter(lambda x: x.attrs['name'].startswith(v.attrs['name'] + '_'), attrs))  # noqa
        return attrs
