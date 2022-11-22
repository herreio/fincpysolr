import logging

from .base import FincIndex
from .docs import FincParser


class FincMain(FincIndex):

    def __init__(self, domain, institution, loglevel=logging.WARNING):
        self.domain = domain.strip("/")
        super().__init__(url="{0}/solr".format(self.domain), core="biblio", name="finc-main", institution=institution, marc=True, loglevel=loglevel)

    def get(self, id, marc=True):
        if marc:
            document = self._get(id, post=self.decode_marc)
        else:
            document = self._get(id)
        if document is not None:
            return FincParser(document, self.institution, marc=marc, ai=False)

    def query_barcode(self, barcode):
        barcode = '"({0}){1}"'.format(self.institution, barcode)
        return self.query('barcode', barcode)

    def query_rsn(self, rsn):
        rsn = '"({0}){1}"'.format(self.institution, rsn)
        return self.query("rsn_id_str_mv", rsn)

    def query_kxp_ppn(self, ppn):
        ppn = '"{0}"'.format(ppn)
        return self.query("kxp_id_str", ppn)

    def query_swb_ppn(self, ppn):
        ppn = '"{0}"'.format(ppn)
        return self.query("swb_id_str", ppn)

    def find_id_by_barcode(self, barcode):
        query = self.query_barcode(barcode)
        return self.find_id(query)

    def find_id_by_rsn(self, rsn):
        query = self.query_rsn(rsn)
        return self.find_id(query)

    def find_id_by_kxp_ppn(self, ppn):
        query = self.query_kxp_ppn(ppn)
        return self.find_id(query)

    def find_id_by_swb_ppn(self, ppn):
        query = self.query_swb_ppn(ppn)
        return self.find_id(query)
