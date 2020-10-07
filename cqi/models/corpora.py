from .attributes import (AlignmentAttributeCollection,
                         PositionalAttributeCollection,
                         StructuralAttributeCollection)
from .ressource import Collection, Model
from .subcorpora import SubcorpusCollection


class Corpus(Model):
    id_attribute = 'api_name'

    @staticmethod
    def _attrs(client, name):
        api_name = name
        return {'api_name': api_name,
                'name': name,
                'size': client.api.cl_attribute_size(
                    '{}.word'.format(api_name)),
                # 'info': client.api.corpus_info(name),
                'charset': client.api.corpus_charset(api_name),
                # 'full_name' = client.api.corpus_full_name(name),
                'properties': client.api.corpus_properties(api_name)}

    def lookups_by_cpos(self, cpos_list, text_count_input=None):
        cpos_list = list(set(cpos_list))
        text_counter = {}
        lookups = {}
        if cpos_list:
            lookups['cpos_lookup'] = {}
        for cpos in cpos_list:
            lookups['cpos_lookup'][cpos] = {}
        for attr in self.positional_attributes.list():
            cpos_attr_values = attr.values_by_cpos(cpos_list)
            for i, cpos in enumerate(cpos_list):
                lookups['cpos_lookup'][cpos][attr.attrs['name']] = \
                    cpos_attr_values[i]
        for attr in self.structural_attributes.list():
            if attr.attrs['has_values']:
                continue
            cpos_attr_ids = attr.ids_by_cpos(cpos_list)
            for i, cpos in enumerate(cpos_list):
                if cpos_attr_ids[i] != -1:
                    lookups['cpos_lookup'][cpos][attr.attrs['name']] = \
                        cpos_attr_ids[i]
                # Count text occurrences.
                # If current cpos is first cpos of a match increment
                # text_counter at corresponding text key by 1.
                # Maybe rework this in the future. Checking if cpos(int) is in
                # a long list is ressource heavy.
                if attr.attrs['name'] == 'text' and text_count_input:
                    # Check if cpos is position one of a match
                    if cpos in text_count_input:
                        # Increment text_counter at corresponding text key by 1
                        text_counter[cpos_attr_ids[i]] = text_counter.get(cpos_attr_ids[i], 0) + 1
            occured_attr_ids = list(filter(lambda x: x != -1,
                                           set(cpos_attr_ids)))
            if not occured_attr_ids:
                continue
            subattrs = \
                self.structural_attributes.list(filters={'part_of': attr})
            if not subattrs:
                continue
            lookup_name = '{}_lookup'.format(attr.attrs['name'])
            lookups[lookup_name] = {}
            for attr_id in occured_attr_ids:
                lookups[lookup_name][attr_id] = {}
            for subattr in subattrs:
                subattr_values = subattr.values_by_ids(occured_attr_ids)
                for i, subattr_value in enumerate(subattr_values):
                    subattr_name = \
                        subattr.attrs['name'][(len(attr.attrs['name']) + 1):]
                    lookups[lookup_name][occured_attr_ids[i]][subattr_name] = \
                        subattr_value
        # Set match_count keyword for text_lookup entries with counted
        # occurrences of text_counter.
        for key in text_counter.keys():
            lookups['text_lookup'][key]['match_count'] = text_counter[key]
        return lookups

    def drop(self):
        return self.client.api.corpus_drop_corpus(self.attrs['api_name'])

    def query(self, query, subcorpus_name='Results'):
        return self.client.api.cqp_query(self.attrs['api_name'],
                                         subcorpus_name, query)

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


class CorpusCollection(Collection):
    model = Corpus

    def get(self, corpus_name):
        return self.prepare_model(self.model._attrs(self.client, corpus_name))

    def list(self):
        return [self.prepare_model(self.model._attrs(self.client, corpus))
                for corpus in self.client.api.corpus_list_coprora()]
