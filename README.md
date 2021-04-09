# Computing term cooccurrence in MEDLINE

This repository quantifies term cooccurrence in MEDLINE.
It's designed for computing the cooccurence of all pairs between two MeSH termsets.
The repository computes MEDLINE cooccurences for the Rephetio hetnet.
See the corresponding [Thinklab discussion](https://doi.org/10.15363/thinklab.d67 "Mining knowledge from MEDLINE articles and their indexed MeSH terms") for more information.

## Modules

+ [`eutility.py`](eutility.py) defines an `esearch_query` function for retreiving PubMed IDs matching a user-defined query.
+ [`cooccurrence.py`](cooccurrence.py) computes the cooccurences bewteen two termsets,
  whose associated PubMed IDs have been retrieved.

## Notebooks

+ [`diseases.ipynb`](diseases.ipynb) computes disease-disease cooccurrence
+ [`symptoms.ipynb`](symptoms.ipynb) computes symptom-disease cooccurrence
+ [`tissues.ipynb`](tissues.ipynb) computes anatomy-disease cooccurrence.
  This notebook depends on `data/disease-pmids.tsv.gz`,
  a dataset created by `symptoms.ipynb`.

## Environment

```shell
# create environment
conda env create --file=environment.yml

# update environment
conda env update --file=environment.yml

# activate environment
conda activate medline

# run jupyter lab for notebook development
jupyter lab
```

## History

On 2021-04-09, ownership of this repository on GitHub was changed from `dhimmel/medline` to `hetio/medline`.
The `hetio` organization has GitHub LFS quota,
providing a more convenient way to store large compressed files.

At the time of the transfer, the only default (and only) branch was `gh-pages`.
The `gh-pages` branch was renamed to `pre-lfs-archive`.
A new default branch `main` was created, whose history has been migrated to use Git LFS.
For the version of this repository used by Project Rephetio to create Hetionet v1.0,
refer to the [v1.0 release](https://github.com/hetio/medline/releases/tag/v1.0).

## Comparison to MRCOC

MEDLINE [produces co-occurrence files](https://ii.nlm.nih.gov/MRCOC.shtml) under the codename MRCOC.
More information is available in the 2016 report [Building an Updated MEDLINE Co-Occurrences (MRCOC) File](https://ii.nlm.nih.gov/MRCOC/MRCOC_Doc_2016.pdf).
These files might be a viable alternative to the analyses in this repository for certain applications.
However, they don't appear to contain topics for supplemental concept records
(for example MeSH term [`C000591739`](https://id.nlm.nih.gov/mesh/2020/C000591739.html)).
Feel free to open an issue with additional insights on or comparisons to MRCOC.

## License

This repository is released under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/ "CC0 1.0 Universal: Public Domain Dedication").
