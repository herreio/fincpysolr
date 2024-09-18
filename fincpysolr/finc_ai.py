import json
import logging

from .base import FincIndex
from .docs import FincParser


class FincAI(FincIndex):

    def __init__(self, domain, institution, core="biblio", name="finc-ai", loglevel=logging.WARNING):
        self.domain = domain.strip("/")
        super().__init__(url="{0}/solr".format(self.domain), core=core, name=name, institution=institution, marc=False, loglevel=loglevel)

    def get(self, id, ims=True):
        if ims:
            document = self._get(id, post=self.decode_ims)
        else:
            document = self._get(id)
        if self.check_institution(document):
            return FincParser(document, self.institution, marc=False, ai=True)

    def decode_ims(self, document):
        if "fullrecord" in document and (
            "recordtype" in document and document["recordtype"] == "is" or
            "record_format" in document and document["record_format"] == "is"):
            try:
                document["fullrecord"] = json.loads(document["fullrecord"])
            except json.JSONDecodeError as err:
                doc_id = None
                if "id" in document:
                    doc_id = document["id"]
                self.logger.exception(err)
                if doc_id is not None:
                    self.logger.error("Parsing intermediate data for document with id '{0}' failed!".format(doc_id))
        return document
