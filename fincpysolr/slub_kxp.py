import logging

from .base import FincIndex
from .docs import FincParser


class SlubKxp(FincIndex):

    def __init__(self, domain, institution="DE-14", loglevel=logging.WARNING):
        self.domain = domain.strip("/")
        super().__init__(url="{0}/solr".format(self.domain), core="slub-kxp", name="slub-kxp", institution=institution, marc=False, loglevel=loglevel)

    def get(self, id):
        document = self._get(id)
        if self.check_institution(document):
            return FincParser(document, self.institution, marc=False, ai=False)
