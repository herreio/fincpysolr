"""
Parse finc Solr documents.
"""

import datetime

from vupysolr.docs import VuFindParser, VuFindMarcParser

DT005 = "%Y%m%d%H%M%S.0"
DT005_NOTIME = "%Y%m%d222222:2"


class FincParser(VuFindParser):
    """
    finc Solr document parser

    For the Solr schema used by finc, see
    https://github.com/finc/index/blob/master/schema.xml
    """

    def __init__(self, doc, isil, marc=False, ai=False):
        self.isil = isil
        super().__init__(doc, marc=marc)
        if marc:
            self.marc = FincMarcParser(self.raw, self.isil)
        self.ai_blob = None
        if ai:
            self.ai_blob = FincArticleParser(self.raw)

    # static fields (finc)

    @property
    def access_facet(self):
        return self._field("access_facet")

    @property
    def barcode(self):
        return self._field("barcode")

    @property
    def barcode_isil(self):
        bcs = self.barcode
        if bcs is not None:
            barcodes = []
            for bc in bcs:
                if bc.startswith("({0})".format(self.isil)):
                    barcodes.append(bc.replace("({0})".format(self.isil), ""))
            if len(barcodes) > 0:
                return barcodes

    @property
    def imprint(self):
        return self._field("imprint")

    @property
    def mega_collection(self):
        return self._field("mega_collection")

    @property
    def record_id(self):
        return self._field("record_id")

    @property
    def rsn(self):
        return self._field("rsn")

    @property
    def rsn_isil(self):
        rsns = self.rsn
        if rsns is not None:
            for rsn in rsns:
                if rsn.startswith("({0})".format(self.isil)):
                    return rsn.replace("({0})".format(self.isil), "")

    @property
    def rvk_facet(self):
        return self._field("rvk_facet")

    @property
    def rvk_label(self):
        return self._field("rvk_label")

    @property
    def rvk_path(self):
        return self._field("rvk_path")

    @property
    def signatur(self):
        return self._field("signatur")

    @property
    def signatur_isil(self):
        signatur = self.signatur
        if signatur is not None:
            signatur_institution = [s.replace("({0})".format(self.isil),"") for s in signatur if self.isil in s]
            if len(signatur_institution) > 0:
                return signatur_institution

    @property
    def source_id(self):
        return self._field("source_id")

    @property
    def zdb(self):
        return self._field("zdb")

    # dynamic fields (custom)

    @property
    def kxp_id_str(self):
        return self._field("kxp_id_str")

    @property
    def swb_id_str(self):
        return self._field("swb_id_str")

    # dynamic fields (finc)

    @property
    def callnumber_isil(self):
        cn_de14 = self._field("callnumber_{0}".format(self.isil.replace("-", "").lower()))
        if type(cn_de14) == list and len(cn_de14) > 0:
            if len(cn_de14) == 1:
                cn_de14 = cn_de14[0]
            return cn_de14

    @property
    def facet_avail(self):
        return self._field("facet_avail")

    @property
    def format_de14(self):
        return self._field_first("format_de14")

    @property
    def format_isil(self):
        return self._field_first("format_{0}".format(self.isil.replace("-", "").lower()))

    # marc fields

    @property
    def marc_holding_location(self):
        if self.marc is not None:
            return self.marc.holding_location

    @property
    def marc_holding_elocation(self):
        if self.marc is not None:
            return self.marc.holding_elocation

    # ai blob fields

    @property
    def ai_blob_rft_date(self):
        if self.ai_blob is not None:
            return self.ai_blob.rft_date

    @property
    def ai_blob_x_date(self):
        if self.ai_blob is not None:
            return self.ai_blob.x_date


class FincMarcParser(VuFindMarcParser):
    """
    finc Solr MARC parser
    """

    def __init__(self, doc, isil):
        self.isil = isil
        super().__init__(doc)

    @property
    def latest_transaction_datetime(self):
        latest_trans = self.latest_transaction
        if latest_trans is not None:
            try:
                return datetime.datetime.strptime(latest_trans, DT005)
            except ValueError:
                try:
                    return datetime.datetime.strptime(latest_trans, DT005_NOTIME)
                except ValueError:  # 00000000000000.0
                    pass

    @property
    def holding_location(self):
        if self.fields is not None:
            for field in self.fields:
                if "852" in field and "subfields" in field["852"]:
                    holding = {}
                    for sf in field["852"]["subfields"]:
                        if "a" in sf and "a" not in holding:
                            holding["a"] = sf["a"]
                        if "x" in sf and "x" not in holding:
                            holding["x"] = sf["x"]
                        if "z" in sf and "z" not in holding:
                            holding["z"] = sf["z"]
                    if "a" in holding and holding["a"] == self.isil:
                        return holding

    @property
    def holding_elocation(self):
        elocations = []
        if self.fields is not None:
            for field in self.fields:
                if "856" in field and "subfields" in field["856"]:
                    holding = {"ind1": field["856"]["ind1"], "ind2": field["856"]["ind2"]}
                    for sf in field["856"]["subfields"]:
                        if "u" in sf and "u" not in holding:
                            holding["u"] = sf["u"]
                        if "x" in sf and "x" not in holding:
                            holding["x"] = sf["x"]
                        if "9" in sf and "9" not in holding:
                            holding["9"] = sf["9"]
                    if "9" in holding and holding["9"] == self.isil:
                        elocations.append(holding)
        if len(elocations) > 0:
            return elocations


class FincArticleParser:
    """
    finc article metadata parser

    For the article metadata schema used by finc, see
    https://github.com/ubleipzig/intermediateschema/blob/master/is-0.9.json
    """

    def __init__(self, doc):
        self.fullrecord = None
        if "fullrecord" in doc:
            self.fullrecord = doc["fullrecord"]

    def _field(self, name):
        if self.fullrecord is not None and type(self.fullrecord) == dict:
            if name in self.fullrecord:
                return self.fullrecord[name]

    def get(self, name):
        return self._field(name)

    @property
    def abstract(self):
        return self._field("abstract")

    @property
    def authors(self):
        return self._field("authors")

    @property
    def doi(self):
        return self._field("doi")

    @property
    def finc_id(self):
        return self._field("finc.id")

    @property
    def finc_record_id(self):
        return self._field("finc.record_id")

    @property
    def finc_source_id(self):
        return self._field("finc.source_id")

    @property
    def languages(self):
        return self._field("languages")

    @property
    def rft_atitle(self):
        return self._field("rft.atitle")

    @property
    def rft_date(self):
        return self._field("rft.date")

    @property
    def rft_epage(self):
        return self._field("rft.epage")

    @property
    def rft_genre(self):
        return self._field("rft.genre")

    @property
    def rft_issn(self):
        return self._field("rft.issn")

    @property
    def rft_jtitle(self):
        return self._field("rft.jtitle")

    @property
    def rft_pages(self):
        return self._field("rft.pages")

    @property
    def rft_pub(self):
        return self._field("rft.pub")

    @property
    def rft_spage(self):
        return self._field("rft.spage")

    @property
    def rft_tpages(self):
        return self._field("rft.tpages")

    @property
    def rft_volume(self):
        return self._field("rft.volume")

    @property
    def ris_type(self):
        return self._field("ris.type")

    @property
    def url(self):
        return self._field("url")

    @property
    def version(self):
        return self._field("version")

    @property
    def x_date(self):
        return self._field("x.date")
