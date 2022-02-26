==========
fincpysolr
==========

``fincpysolr`` allows to access finc Solr documents in Python and is intended for
librarians and IT staff of institutions participating in finc. For more
information on finc, see their `website <https://finc.info>`_ (german),
`Wikipedia article <https://en.wikipedia.org/wiki/Finc>`_ (english) or
find them on `GitHub <https://github.com/finc>`_.

For using this package, access (via proxy if you like) to the finc Solr infrastructure
hosted by the `Leipzig University Library <https://github.com/ubleipzig>`_ is required.

In the `usage example`_ below, an imaginary member of the finc consortium
is used. It is identified by the the not yet assigned ISIL
`DE-9999 <https://sigel.staatsbibliothek-berlin.de/suche/?q=isil%3DDE-9999>`_.
Just replace the two index domains and the library code with the values of your
institution to get started.

Installation
============

... via SSH
~~~~~~~~~~~

.. code-block:: bash

   pip install -e git+ssh://git@github.com/herreio/fincpysolr.git#egg=fincpysolr

... or via HTTPS
~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -e git+https://github.com/herreio/fincpysolr.git#egg=fincpysolr

Usage Example
=============

.. code-block:: python

    import fincpysolr


*Create finc Solr clients*

.. code-block:: python

    ai_domain = "https://finc-ai.index.anwender.de"                      # replace dummy
    main_domain = "https://finc-main.index.anwender.de"                  # replace dummy
    institution = "DE-9999"                                              # replace dummy
    cluster = fincpysolr.cluster(ai_domain, main_domain, institution)


*Retrieve finc Solr document*

.. code-block:: python

    doc_id = "0-123456789"                                               # replace dummy
    doc = cluster.get(doc_id)


*Inspect finc Solr document*

.. code-block:: python

    # print document title
    print(doc.title)
    # print timestamp of last indexation
    print(doc.last_indexed)
    # print identifier of record
    print(doc.record_id)
    # print identifier of record source
    print(doc.source_id)
    # print resource link of institution (marcfinc)
    print(doc.marc_holding_elocation)


Dependency
==========

This package is built on top of |vupysolr|_ (`PyPI <https://pypi.org/project/vupysolr/>`_).

.. |vupysolr| replace:: ``vupysolr``
.. _vupysolr: https://github.com/herreio/vupysolr
