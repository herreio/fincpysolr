"""
Access finc Solr indexes.
"""

import logging
from .docs import FincParser
from vupysolr import VuFindIndex, VuFindCluster
from vupysolr.utils import get_logger


class FincIndex(VuFindIndex):

    def __init__(self, url="http://localhost:8983/solr", core="biblio", name="default", institution="DE-14", marc=False, loglevel=logging.WARNING):
        self.institution = institution
        super().__init__(url=url, core=core, name=name, marc=marc, loglevel=loglevel)
        self.logger = get_logger("fincpysolr", loglevel=loglevel)

    def get(self, id):
        if self.marc:
            document = self._get(id, post=self.decode_marc)
        else:
            document = self._get(id)
        document = self._get(id)
        if self.check_institution(document):
            return FincParser(document, self.institution)

    def find_doc(self, query, **kwargs):
        response = self.search(query, **kwargs)
        if response is not None:
            if len(response.docs) > 0:
                if len(response.docs) == 1:
                    document = response.docs[0]
                    if self.check_institution(document):
                        return FincParser(document, self.institution)
                else:
                    self.logger.warning("Found multiple documents matching query {0}".format(query))

    def check_institution(self, document):
        if document is not None:
            if "institution" in document:
                if self.institution in document["institution"]:
                    return True
        return False


class FincCluster(VuFindCluster):

    def __init__(self, idx=None):
        super().__init__(idx)
