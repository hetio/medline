import itertools

import scipy.stats
import pandas

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

        a = len(pmids0 & pmids1)
        b = len(pmids0) - a
        c = len(pmids1) - a
        d = total_pmids - len(pmids0 | pmids1)
        contingency_table = [[a, b], [c, d]]

        expected = len(pmids0) * len(pmids1) / total_pmids
        enrichment = a / expected

        oddsratio, pvalue = scipy.stats.fisher_exact(contingency_table, alternative='greater')
        rows.append([term0, term1, a, expected, enrichment, oddsratio, pvalue])

    columns = [term0_name, term1_name, 'cooccurrence', 'expected', 'enrichment', 'odds_ratio', 'p_fisher']
    df = pandas.DataFrame(rows, columns=columns)

    if verbose:
        print('\nCooccurrence scores calculated for {} {} -- {} pairs'.format(len(df), term0_name, term1_name))
    return df
