from setuptools import setup
from outbreaker import __version__, _program

setup(
    name='outbreaker',
    version=__version__,
    packages=['outbreaker'],
    package_dir={'outbreaker': 'outbreaker'},
    scripts=["outbreaker/workflows/outbreaker.smk",
    "outbreaker/workflows/outbreaker_summary_report.Rmd"],
    url='',
    license='',
    author='Matthew Watson',
    author_email='matthew.watson@oahpp.ca',
    description='snakemake and Python integrated workflow for intermediate file generation for COVID outbreak analysis',
    install_requires = ["pandas>=1.1.5", "numpy>=1.19", "biopython>=1.79"],
    entry_points="""
    [console_scripts]
    {program} = outbreaker.main:main
    """.format(program=_program),
    include_package_data=True,
)
