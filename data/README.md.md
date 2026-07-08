# data/

This project's model is parameter-driven rather than dataset-driven: pathway
impacts are calculated from literature-derived emission factors and process
yields (see `src/parameters.py`), not from a raw input dataset.

The subfolders below are kept for structure and for future extension
(e.g. if region-specific or facility-level data is incorporated later):

- `raw/` — would hold unprocessed source data, if/when added.
- `processed/` — would hold cleaned/derived data.
- `external/` — would hold third-party reference datasets (e.g. regional
  grid emission factors), if incorporated in a future iteration.

No data files are currently required to reproduce this project's results.
