from .ressource import Collection, Model
from ..api.specification import (CONST_FIELD_KEYWORD, CONST_FIELD_MATCH,
                                 CONST_FIELD_MATCHEND, CONST_FIELD_TARGET)


class Subcorpus(Model):
    id_attribute = 'api_name'

    @staticmethod
    def _attrs(client, corpus, name):
        api_name = '{}:{}'.format(corpus.attrs['api_name'], name)
        fields = {}
        if client.api.cqp_subcorpus_has_field(api_name, CONST_FIELD_MATCH):
            fields['match'] = CONST_FIELD_MATCH
        if client.api.cqp_subcorpus_has_field(api_name,
                                              CONST_FIELD_MATCHEND):
            fields['matchend'] = CONST_FIELD_MATCHEND
        if client.api.cqp_subcorpus_has_field(api_name, CONST_FIELD_TARGET):
            fields['target'] = CONST_FIELD_TARGET
        if client.api.cqp_subcorpus_has_field(api_name, CONST_FIELD_KEYWORD):
            fields['keyword'] = CONST_FIELD_KEYWORD
        return {'api_name': api_name,
                'name': name,
                'fields': fields,
                'size': client.api.cqp_subcorpus_size(api_name)}

    def drop(self):
        return self.client.api.cqp_drop_subcorpus(self.attrs['api_name'])

    def dump(self, field, first, last):
        return self.client.api.cqp_dump_subcorpus(self.attrs['api_name'],
                                                  field, first, last)

    def export(self, context=25, cutoff=float('inf'), expand_lists=False,
               offset=0):
        if self.attrs['size'] == 0:
            return {"matches": []}
        first_match = max(0, offset)
        last_match = min((offset + cutoff - 1), (self.attrs['size'] - 1))
        match_boundaries = zip(self.dump(self.attrs['fields']['match'],
                                         first_match, last_match),
                               self.dump(self.attrs['fields']['matchend'],
                                         first_match, last_match))
        context_cpos_list = []
        match_cpos_list = []
        text_count_matches = []
        matches = []
        for match_start, match_end in match_boundaries:
            match_cpos_list += list(range(match_start, (match_end + 1)))
            c = (match_start, match_end)
            lc = rc = None
            lc_rbound = max(0, (match_start - 1))
            if lc_rbound != match_start:
                lc_lbound = max(0, (match_start - context))
                lc = (lc_lbound, lc_rbound)
                context_cpos_list_lc = list(range(lc_lbound, lc_rbound + 1))
            rc_lbound = min((match_end + 1),
                            (self.collection.corpus.attrs['size'] - 1))
            if rc_lbound != match_end:
                rc_rbound = min((match_end + context),
                                (self.collection.corpus.attrs['size'] - 1))
                rc = (rc_lbound, rc_rbound)
                context_cpos_list_rc = list(range(rc_lbound, rc_rbound + 1))
            context_cpos_list += context_cpos_list_lc
            context_cpos_list += context_cpos_list_rc
            if expand_lists:
                match = {'lc': list(range(lc[0], (lc[1] + 1))),
                         'c': list(range(c[0], (c[1] + 1))),
                         'rc': list(range(rc[0], (rc[1] + 1)))}
            else:
                match = {'lc': lc, 'c': c, 'rc': rc}
            text_count_matches.append(c[0])
            matches.append(match)
        if context > 0:
            context_lookups = self.collection.corpus.lookups_by_cpos(set(context_cpos_list))
        match_lookups = self.collection.corpus.lookups_by_cpos(set(match_cpos_list), text_count_matches)
        match_lookups['cpos_lookup'].update(context_lookups['cpos_lookup'])
        return {'matches': matches, **match_lookups}

    def fdist_1(self, cutoff, field, attribute):
        return self.client.api.cqp_fdist_1(self.attrs['api_name'], cutoff,
                                           field, attribute._name)

    def fdist_2(self, cutoff, field_1, attribute_1, field_2, attribute_2):
        return self.client.api.cqp_fdist_2(self.attrs['api_name'], cutoff,
                                           field_1, attribute_1._name,
                                           field_2, attribute_2._name)


class SubcorpusCollection(Collection):
    model = Subcorpus

    def __init__(self, client=None, corpus=None):
        super(SubcorpusCollection, self).__init__(client=client)
        self.corpus = corpus

    def get(self, subcorpus_name):
        return self.prepare_model(self.model._attrs(self.client, self.corpus,
                                                    subcorpus_name))

    def list(self):
        return [self.prepare_model(self.model._attrs(self.client, self.corpus, subcorpus))  # noqa
                for subcorpus in self.client.api.cqp_list_subcorpora(self.corpus.attrs['api_name'])]  # noqa
