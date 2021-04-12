import itertools
from typing import Any, Dict, List, Set

import scipy.stats
import pandas


def read_pmids_tsv(path, key, min_articles = 1):
    term_to_pmids = dict()
    pmids_df = pandas.read_table(path, compression='gzip')
    pmids_df = pmids_df[pmids_df.n_articles >= min_articles]
    for i, row in pmids_df.iterrows():
        term = row[key]
        pmids = row.pubmed_ids.split('|')
        term_to_pmids[term] = set(pmids)
    pmids_df.drop('pubmed_ids', axis=1, inplace=True)
    return pmids_df, term_to_pmids

def score_pmid_cooccurrence(term0_to_pmids, term1_to_pmids, term0_name='term_0', term1_name='term_1', verbose=True):
    """
    Find pubmed cooccurrence between topics of two classes.

    term0_to_pmids -- a dictionary that returns the pubmed_ids for each term of class 0
    term0_to_pmids -- a dictionary that returns the pubmed_ids for each term of class 1
    """
    all_pmids0 = set.union(*term0_to_pmids.values())
    all_pmids1 = set.union(*term1_to_pmids.values())
    pmids_in_both = all_pmids0 & all_pmids1
    total_pmids = len(pmids_in_both)
    if verbose:
        print('Total articles containing a {}: {}'.format(term0_name, len(all_pmids0)))
        print('Total articles containing a {}: {}'.format(term1_name, len(all_pmids1)))
        print('Total articles containing both a {} and {}: {}'.format(term0_name, term1_name, total_pmids))

    term0_to_pmids = term0_to_pmids.copy()
    term1_to_pmids = term1_to_pmids.copy()
    for d in term0_to_pmids, term1_to_pmids:
        for key, value in list(d.items()):
            d[key] = value & pmids_in_both
            if not d[key]:
                del d[key]

    if verbose:
        print('\nAfter removing terms without any cooccurences:')
        print('+ {} {}s remain'.format(len(term0_to_pmids), term0_name))
        print('+ {} {}s remain'.format(len(term1_to_pmids), term1_name))

    rows = list()
    for term0, term1 in itertools.product(term0_to_pmids, term1_to_pmids):
        pmids0 = term0_to_pmids[term0]
        pmids1 = term1_to_pmids[term1]
        row = {
            term0_name: term0,
            term1_name: term1,
            **cooccurrence_metrics(pmids0, pmids1, total_pmids=total_pmids)
        }
        rows.append(row)
    df = pandas.DataFrame(rows)

    if verbose:
        print('\nCooccurrence scores calculated for {} {} -- {} pairs'.format(len(df), term0_name, term1_name))
    return df


def cooccurrence_metrics(source_pmids: Set[str], target_pmids: Set[str], total_pmids: int) -> Dict[str, Any]:
    """
    Compute metrics of cooccurrence between two sets of pubmed ids.
    Requires providing the total number of pubmed ids in the corpus.
    """
    a = len(source_pmids & target_pmids)
    b = len(source_pmids) - a
    c = len(target_pmids) - a
    d = total_pmids - (a + b + c)
    contingency_table = [[a, b], [c, d]]
    # discussion on this formula in https://github.com/hetio/medline/issues/1
    expected = len(source_pmids) * len(target_pmids) / total_pmids
    enrichment = a / expected
    odds_ratio, p_fisher = scipy.stats.fisher_exact(contingency_table, alternative='greater')
    return {
        "cooccurrence": a,
        "expected": expected,
        "enrichment": enrichment,
        "odds_ratio": odds_ratio,
        "p_fisher": p_fisher,
        "n_source": len(source_pmids),
        "n_target": len(target_pmids),
    }
