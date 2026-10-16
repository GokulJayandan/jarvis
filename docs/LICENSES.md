# Licences and attribution

* Official code/docs: MIT, Copyright 2026 RomeoJulietLove. Original notice in
  `LICENSE`; file-level provenance in `results/provenance.json`.
* Supplied synthetic data: `DATA_LICENSE.md`; preserve invented-data provenance and
  identify modifications. Records and published checksums are unchanged.
* Vendored NetworkX 3.6.1 blossom: BSD-3-Clause, full notice at
  `raven/vendor/LICENSE.networkx`. Extraction script and checksums are included.
* Python interpreter/standard library: Python Software Foundation licence. Docker
  base is the official `python:3.12.7-slim` image. The actual Linux container build and official evaluation succeeded in
  [CI run 38919907335](https://github.com/GokulJayandan/jarvis/actions/runs/38919907335); image identity and validation scope are
  recorded in `CI_VALIDATION.md`.
* Experiment-only dependencies are pinned in `requirements-dev.txt`. NetworkX,
  NumPy, contourpy and cycler use BSD-style licences; matplotlib uses its PSF-based
  licence; psutil uses BSD-3-Clause; Pillow 12.3.0 declares MIT-CMU; fonttools uses MIT; kiwisolver
  uses BSD-3-Clause; packaging uses Apache-2.0/BSD; pyparsing and six use MIT;
  python-dateutil uses Apache-2.0/BSD. Installed distribution licence metadata is
  captured by `scripts/dependency_licenses.py` for exact notices.
  NumPy's distribution also declares 0BSD, MIT, Zlib and CC0-1.0 components; see
  the exported exact metadata rather than treating this short summary as exhaustive.

New Team Jarvis work remains owned by its authors. The upstream MIT notice does
not automatically grant a commercial licence to student work, consistent with
the official competition statement. No outside personal data or pretrained assets
are included. AI coding assistance: OpenAI Codex; all experiment numbers must derive
from stored executed outputs rather than generated claims.
