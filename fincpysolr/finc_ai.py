import logging

from .base import FincIndex
from .docs import FincParser

from vupysolr.utils import json_req


class FincAI(FincIndex):

    def __init__(self, domain, institution, loglevel=logging.WARNING):
        self.domain = domain.strip("/")
        self.url_blob = "{0}/blob".format(self.domain)
        super().__init__(url="{0}/solr".format(self.domain), core="biblio", name="finc-ai", institution=institution, marc=False, loglevel=loglevel)

    def get(self, id, blob=False):
        document = self._get(id)
        if blob and document is not None:
            if "fullrecord" in document:
                fullrec_id = document["fullrecord"]
                if type(fullrec_id) == str and fullrec_id.startswith("blob:"):
                    blob_id = fullrec_id.split(":")[1]
                    fullrecord = self._get_blob(blob_id)
                    if fullrecord is not None:
                        document["fullrecord"] = fullrecord
        if document is not None and self.check_institution(document):
            return FincParser(document, self.institution, marc=False, ai=blob)

    def get_blob_url(self, id):
        return "{0}?{1}".format(self.url_blob, id)

    def _get_blob(self, id):
        self.logger.info("Fetch fullrecord from blob store of Solr index finc-ai.")
        url = self.get_blob_url(id)
        return json_req(url)
