# CQi SDK for Python

A Python library for the [IMS Open Corpus Workbench](http://cwb.sourceforge.net/) (CWB) [corpus query interface](http://cwb.sourceforge.net/cqi.php) (CQi) API.

## Installation

The latest stable version [is available on PyPI](https://pypi.python.org/pypi/cqi/). Either add `cqi` to your `requirements.txt` file or install with pip:

```
pip install cqi
```

## Version compatibility

| Package version | Protocol version |
|-----------------|------------------|
| 0.1.0           | 0.1              |
| 0.1.1           | 0.1              |

## Usage

```python
import cqi


client = cqi.CQiClient('127.0.0.1')
client.connect(username='anonymous', password='') # 258 ~ CQI_STATUS_CONNECT_OK
client.ping() # 260 ~ CQI_STATUS_PING_OK
corpus = client.corpora.get('CORPUS') # <Corpus: CORPUS>
corpus.query('"and" []* "the";', 'Results') # 257 ~ CQI_STATUS_OK
results = corpus.subcorpora.get('Results') # <Subcorpus: CORPUS:Results>
client.disconnect() # 259 ~ CQI_STATUS_BYE_OK
```
