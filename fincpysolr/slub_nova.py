import logging

from .base import FincIndex
from .docs import FincParser


class SlubNova(FincIndex):

    def __init__(self, core, domain, institution="DE-14", loglevel=logging.WARNING):
        self.domain = domain.strip("/")
        super().__init__(url="{0}/solr".format(self.domain), core=core,
                         name=core, institution=institution, marc=False,
                         loglevel=loglevel)

    def get(self, id, marc=False, ai=False):
        document = self._get(id)
        if self.check_institution(document):
            return FincParser(document, self.institution, marc=marc, ai=ai)
