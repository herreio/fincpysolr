==========
fincpysolr
==========

``fincpysolr`` allows to access finc Solr documents and is intended for
librarians and IT staff of institutions participating in finc. For more
information on finc, see https://finc.info.

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
    # print first entry date (marcfinc)
    print(doc.marc_date_entered_iso)
