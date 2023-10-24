import logging

from .base import FincIndex
from .docs import FincParser


class SlubMain(FincIndex):

    def __init__(self, domain, institution="DE-14", loglevel=logging.WARNING):
        self.domain = domain.strip("/")
        super().__init__(url="{0}/solr".format(self.domain), core="slub-main", name="slub-main", institution=institution, marc=True, loglevel=loglevel)

    def get(self, id, marc=True):
        if marc:
            document = self._get(id, post=self.decode_marc)
        else:
            document = self._get(id)
        if self.check_institution(document):
            return FincParser(document, self.institution, marc=marc, ai=False)
