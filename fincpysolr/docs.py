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
        self.isil_slim = self._isil_slim(isil)
        self.isil_pattern = self._isil_pattern(isil)
        super().__init__(doc, marc=marc)
        if marc:
            self.marc = FincMarcParser(self.raw, self.isil)
        self.ai_blob = None
        if ai:
            self.ai_blob = FincArticleParser(self.raw)

    @staticmethod
    def _isil_slim(isil):
        return isil.replace("-", "").lower()

    @staticmethod
    def _isil_pattern(isil):
        return "({0})".format(isil)

    @staticmethod
    def _isil_replace(target, isil):
        return target.replace("({0})".format(isil), "")

    # static fields (vufind)

    @property
    def building_isil(self):
        bs = self.building
        if bs is not None:
            buildings = []
            for b in bs:
                if b.startswith(self.isil_pattern):
                    buildings.append(b.replace(self.isil_pattern, ""))
            if len(buildings) > 0:
                return buildings

    def _ctrlnum_isil(self, isil, unique=True):
        ctrlnums = self.ctrlnum
        if ctrlnums is not None:
            isil_ctrl = []
            for ctrln in ctrlnums:
                if ctrln.startswith(self._isil_pattern(isil)):
                    isil_ctrl.append(self._isil_replace(ctrln, isil))
            if len(isil_ctrl) > 0:
                if len(isil_ctrl) == 1 and unique:
                    isil_ctrl = isil_ctrl[0]
                return isil_ctrl

    @property
    def ctrlnum_bsz(self):
        return self._ctrlnum_isil("DE-576")

    @property
    def ctrlnum_kxp(self):
        return self._ctrlnum_isil("DE-627")

    @property
    def ctrlnum_agv(self):
        return self._ctrlnum_isil("DE-599", unique=False)

    @property
    def ctrlnum_oclc(self):
        return self._ctrlnum_isil("OCoLC", unique=False)

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
                if bc.startswith(self.isil_pattern):
                    barcodes.append(bc.replace(self.isil_pattern, ""))
            if len(barcodes) > 0:
                return barcodes

    @property
    def finc_class_facet(self):
        return self._field("finc_class_facet")

    @property
    def imprint(self):
        return self._field("imprint")

    @property
    def mega_collection(self):
        return self._field("mega_collection")

    @property
    def publish_place(self):
        return self._field("publishPlace")

    @property
    def purchase(self):
        return self._field("purchase")

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
                if rsn.startswith(self.isil_pattern):
                    return rsn.replace(self.isil_pattern, "")

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

    def _signatur_isil(self, isil):
        signatur = self.signatur
        if signatur is not None:
            signatur_isil = [s.replace(self._isil_pattern(isil), "")
                             for s in signatur if s.startswith(self._isil_pattern(isil))]
            if len(signatur_isil) > 0:
                return signatur_isil

    @property
    def signatur_isil(self):
        return self._signatur_isil(self.isil)

    @property
    def source_id(self):
        return self._field("source_id")

    @property
    def topic_id(self):
        return self._field("topic_id")

    @property
    def topic_ref(self):
        return self._field("topic_ref")

    @property
    def urn(self):
        return self._field("urn")

    @property
    def zdb(self):
        return self._field("zdb")

    # dynamic fields (vufind)

    @property
    def finc_id_str(self):
        return self._field("finc_id_str")

    @property
    def kxp_id_str(self):
        return self._field("kxp_id_str")

    @property
    def match_str(self):
        return self._field("match_str")

    @property
    def swb_id_str(self):
        return self._field("swb_id_str")

    @property
    def title_list_str(self):
        return self._field("title_list_str")

    @property
    def title_part_str(self):
        return self._field("title_part_str")

    @property
    def fincclass_txtF_mv(self):
        return self._field("fincclass_txtF_mv")

    # dynamic fields (finc)

    @property
    def branch_de14(self):
        br_isil = self._field("branch_de14")
        if type(br_isil) == list and len(br_isil) > 0:
            return br_isil

    @property
    def branch_de15(self):
        br_isil = self._field("branch_de15")
        if type(br_isil) == list and len(br_isil) > 0:
            return br_isil

    @property
    def branch_isil(self):
        br_isil = self._field("branch_{0}".format(self.isil_slim))
        if type(br_isil) == list and len(br_isil) > 0:
            return br_isil

    @property
    def callnumber_de14(self):
        cn_de14 = self._field("callnumber_de14")
        if type(cn_de14) == list and len(cn_de14) > 0:
            return cn_de14

    @property
    def callnumber_de15(self):
        cn_de15 = self._field("callnumber_de15")
        if type(cn_de15) == list and len(cn_de15) > 0:
            return cn_de15

    @property
    def callnumber_isil(self):
        cn_isil = self._field("callnumber_{0}".format(self.isil_slim))
        if type(cn_isil) == list and len(cn_isil) > 0:
            return cn_isil

    @property
    def facet_avail(self):
        return self._field("facet_avail")

    @property
    def facet_de14_branch_collcode_exception(self):
        return self._field("facet_de14_branch_collcode_exception")

    @property
    def format_finc(self):
        return self._field_first("format_finc")

    @property
    def format_de14(self):
        return self._field_first("format_de14")

    @property
    def format_de15(self):
        return self._field_first("format_de15")

    @property
    def format_isil(self):
        return self._field_first("format_{0}".format(self.isil_slim))

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
