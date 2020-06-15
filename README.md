# CQi SDK for Python

A Python library for the [IMS Open Corpus Workbench](http://cwb.sourceforge.net/) (CWB) [corpus query interface](http://cwb.sourceforge.net/cqi.php) (CQi) API.

## Installation

The latest stable version [is available on PyPI](https://pypi.python.org/pypi/cqi/). Either add `cqi` to your `requirements.txt` file or install with pip:

    pip install cqi

## Usage

```python
>>> client.connect(username='anonymous', password='')
{'code': 258, 'msg': 'CQI_STATUS_CONNECT_OK'}
client.ping()
{'code': 260, 'msg': 'CQI_STATUS_PING_OK'}
>>> corpus = client.corpora.get('CORPUS')
<Corpus: CORPUS>
>>> corpus.query('"and" []* "the";')
{'code': 257, 'msg': 'CQI_STATUS_OK'}
>>> results = corpus.subcorpora.get('Results')
<Subcorpus: CORPUS:Results>
>>> lib = results.export(context=25, cutoff=1, offset=0)
{'match': {'lc': (<cpos_lbound>, <cpos_rbound>),
           'c': (<cpos_lbound>, <cpos_rbound>),
           'rc': (<cpos_lbound>, <cpos_rbound>)},
 'cpos_lookup': {<cpos>: {<p_attr>: <p_attr_value>,
                          ...
                          <s_attr>: <s_attr_id>,
                          ...},
                 ...},
 '<s_attr>_lookup': {<s_attr_id>: {<sub_s_attr>: <sub_s_attr_value>,
                                   ...},
                     ...}}
>>> s = corpus.structural_attributes.get('s')
<StructuralAttribute: CORPUS.s>
>>> lib = s.export(105, 120, context=3)
{'match': {'lc': (<cpos_lbound>, <cpos_rbound>),
           'c': (<cpos_lbound>, <cpos_rbound>),
           'rc': (<cpos_lbound>, <cpos_rbound>)},
 'cpos_lookup': {<cpos>: {<p_attr>: <p_attr_value>,
                          ...
                          <s_attr>: <s_attr_id>,
                          ...},
                 ...},
 '<s_attr>_lookup': {<s_attr_id>: {<sub_s_attr>: <sub_s_attr_value>,
                                   ...},
                     ...}}
>>> client.disconnect()
{'code': 259, 'msg': 'CQI_STATUS_BYE_OK'}
```
