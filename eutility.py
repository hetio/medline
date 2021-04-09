import time

import xml.etree.ElementTree as ET

import requests

def esearch_query(payload, retmax = 100, sleep=2):
    """
    Query the esearch E-utility.
    NOTE: use `pubmedpy.eutilities.esearch_query` instead.
    This function might be deleted in the future.
    """
    url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    payload['retmax'] = retmax
    payload['retstart'] = 0
    ids = list()
    count = 1
    while payload['retstart'] < count:
        response = requests.get(url, params=payload)
        xml = ET.fromstring(response.content)
        count = int(xml.findtext('Count'))
        ids += [xml_id.text for xml_id in xml.findall('IdList/Id')]
        payload['retstart'] += retmax
        time.sleep(sleep)
    return ids
