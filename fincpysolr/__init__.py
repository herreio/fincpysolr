"""
Access finc Solr documents.

For more information on finc, see https://finc.info.
"""

__author__ = "Donatus Herre <donatus.herre@slub-dresden.de>"
__version__ = "0.1.13"

from .finc_ai import FincAI
from .finc_main import FincMain
from .slub_kxp import SlubKxp
from .base import FincCluster
from .docs import FincParser


def parse(doc, isil, marc=False, ai=False):
    return FincParser(doc, isil, marc=marc, ai=ai)


def parse_de14(doc, marc=False, ai=False):
    return FincParser(doc, "DE-14", marc=marc, ai=ai)


def cluster(finc_ai_domain, finc_main_domain, isil, loglevel=0):
    finc_ai = FincAI(finc_ai_domain, isil, loglevel=loglevel)
    finc_main = FincMain(finc_main_domain, isil, loglevel=loglevel)
    return FincCluster([finc_ai, finc_main])


def cluster_de14(finc_ai_domain, finc_main_domain, slub_kxp_domain, loglevel=0):
    finc_ai = FincAI(finc_ai_domain, "DE-14", loglevel=loglevel)
    finc_main = FincMain(finc_main_domain, "DE-14", loglevel=loglevel)
    slub_kxp = SlubKxp(slub_kxp_domain, "DE-14", loglevel=loglevel)
    return FincCluster([finc_ai, finc_main, slub_kxp])
