# CQi SDK for Python

A Python library for the [IMS Open Corpus Workbench](http://cwb.sourceforge.net/) (CWB) [Corpus Query Interface](https://cwb.sourceforge.io/documentation.php#cqi) (CQi) API.

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
| 0.1.2           | 0.1              |
| 0.1.3           | 0.1              |

## Usage

```python
import cqi


client = cqi.CQiClient('127.0.0.1')
client.connect(username='anonymous', password='') # <class 'cqi.status.StatusConnectOk'>
client.ping() # <class 'cqi.status.StatusPingOk'>
corpus = client.corpora.get('CORPUS') # <Corpus: CORPUS>
corpus.query('"and" []* "the";', 'Results') # <class 'cqi.status.StatusOk'>
results = corpus.subcorpora.get('Results') # <Subcorpus: CORPUS:Results>
client.disconnect() # <class 'cqi.status.StatusByeOk'>
```
