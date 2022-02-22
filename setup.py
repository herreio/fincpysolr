import setuptools

setuptools.setup(
    name="fincpysolr",
    version="0.1.0",
    author="Donatus Herre",
    author_email="donatus.herre@slub-dresden.de",
    description="Access finc Solr documents.",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    license=open("LICENSE").read(),
    url="https://github.com/herreio/fincpysolr",
    packages=["fincpysolr"],
    install_requires=["vupysolr @ git+https://github.com/herreio/vupysolr@main"],
)