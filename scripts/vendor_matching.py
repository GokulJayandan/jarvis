"""Reproduce the minimal BSD-licensed solver extraction from pinned NetworkX."""
import hashlib
import inspect
import json
from pathlib import Path
import networkx as nx
from networkx.algorithms.matching import matching_dict_to_set

root=Path(__file__).resolve().parents[1]
destination=root/'raven'/'vendor'
source=inspect.getsource(inspect.unwrap(nx.max_weight_matching))
source=source[source.index('def max_weight_matching'):]
helper=inspect.getsource(matching_dict_to_set)
header='"""Vendored NetworkX 3.6.1 blossom; BSD-3-Clause, see LICENSE.networkx.\nOnly decorators removed; algorithm body unchanged. Minimal graph API in matching.py.\n"""\nfrom itertools import repeat\n\n'
(destination/'blossom.py').write_text(header+helper+'\n'+source,encoding='utf-8',newline='\n')
dist=next(Path(nx.__file__).parents[1].glob('networkx-*.dist-info'))
license_file=next(p for p in dist.rglob('LICENSE*') if p.is_file())
(destination/'LICENSE.networkx').write_bytes(license_file.read_bytes())
(destination/'provenance.json').write_text(json.dumps({'version':nx.__version__,
    'source':'https://github.com/networkx/networkx/blob/networkx-3.6.1/networkx/algorithms/matching.py',
    'original_function_sha256':hashlib.sha256(inspect.getsource(inspect.unwrap(nx.max_weight_matching)).encode()).hexdigest(),
    'local_sha256':hashlib.sha256((destination/'blossom.py').read_bytes()).hexdigest(),
    'modifications':['Removed dispatch and graph-type decorators; unchanged algorithm and helper.']},indent=2)+'\n')
