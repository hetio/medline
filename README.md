# Computing term cooccurrence in MEDLINE

This repository quantifies term cooccurrence in MEDLINE. It's designed for computing the cooccurence of all pairs between two MeSH termsets. The repository computes MEDLINE cooccurences for the Rephetio hetnet. See the corresponding [Thinklab discussion](https://doi.org/10.15363/thinklab.d67 "Mining knowledge from MEDLINE articles and their indexed MeSH terms") for more information.

## Modules

+ [`eutility.py`](eutility.py) defines an `esearch_query` function for retreiving PubMed IDs matching a user-defined query.
+ [`cooccurrence.py`](cooccurrence.py) computes the cooccurences bewteen two termsets, whose associated PubMed IDs have been retrieved.

## Notebooks

+ [`diseases.ipynb`](diseases.ipynb) computes disease-disease cooccurrence
+ [`symptoms.ipynb`](symptoms.ipynb) computes symptom-disease cooccurrence
+ [`tissues.ipynb`](tissues.ipynb) computes anatomy-disease cooccurrence. This notebook depends on `data/disease-pmids.tsv.gz`, a dataset created by `symptoms.ipynb`.

## License

This repository is released under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/ "CC0 1.0 Universal: Public Domain Dedication").
