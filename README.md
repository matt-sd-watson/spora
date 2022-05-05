# outbreaker

![example workflow](https://github.com/matt-sd-watson/outbreaker/actions/workflows/main.yml/badge.svg)

snakemake and Python integrated workflow for intermediate file generation for COVID outbreak analysis

## Installation

```
git clone https://github.com/matt-sd-watson/outbreaker.git
conda env create -f ncov_outbreaker/environments/environment.yml
conda activate ncov_outbreaker
cd outbreaker
pip install . 
```

## Updating

```
conda activate ncov_outbreaker
cd ~/outbreaker
git checkout main
git pull
pip install . 
```

## Usage
```
usage: 
    	outbreaker -c <config.yaml> 
    	OR
    	outbreaker --focal_list ...<input args>

Outbreaker: Python and snakemake outbreak workflow for COVID-19

optional arguments:
  -h, --help            Show the help output and exit.
  -c CONFIG, --config CONFIG
                        Input config file in yaml format, all command line arguments can be passed via the config file.
  -f FOCAL_SEQS, --focal-sequences FOCAL_SEQS
                        Input .txt list or multi-FASTA focal samples for outbreak. Required
  -b BACKGROUND_SEQS, --background-sequences BACKGROUND_SEQS
                        Optional input .txt list or multi-FASTA background samples to add to analysis
  -m MASTER_FASTA, --master-fasta MASTER_FASTA
                        Master FASTA of genomic sequences to select from. Required if either --focal-sequences or --background-sequences are not supplied in
                        FASTA format
  -o OUTDIR, --output-directory OUTDIR
                        Path to the desired output directory. If none is provided, a new folder named outbreaker will be created in the current directory
  -r REFERENCE, --reference REFERENCE
                        .gb file containing the desired COVID-19 reference sequence. Required
  -p PREFIX, --prefix PREFIX
                        Prefix string to label all output files. Default: outbreak
  -t NTHREADS, --nthreads NTHREADS
                        Number of threads to use for processing. Default: 4
  -s, --snps-only       Generate a snps-only FASTA from the input FASTA. Default: False
  -rn, --rename         Rename the FASTA headers to be compatible with NML standards. Default: False
  -nc NAMES_CSV, --names-csv NAMES_CSV
                        Use the contents of a CSV to rename the input FASTA. Requires the following column headers: original_name, new_name
  -ncs, --no-constant-sites
                        Do not enable constant sites to be used for SNPs only tree generation. Default: Enabled
  -fi, --filter         Filter both the focal and background sequences based on genome completeness and length. Default: Not enabled
  -gc GENOME_COMPLETENESS, --genome-completeness GENOME_COMPLETENESS
                        Integer for the minimum genome completeness percentage for filtering. Default: 90
  -gl GENOME_LENGTH, --genome-length GENOME_LENGTH
                        Integer for the minimum genome length for filtering. Default: 29500
  -rp, --report         Generate a summary output report for the outbreaker run. Default: Not enabled
  -v, --version         Show the current outbreaker version then exit.
```

## Documentation

More detailed documentation for outbreaker usage and functionality can be found [here](docs/0-OVERVIEW.md)

## Acknowledgments

Inspiration for code structure and design for outbreaker was inspired by [pangolin](https://github.com/cov-lineages/pangolin) and [civet](https://github.com/artic-network/civet), and minor code blocks were adopted from these software.

The **Background** section in the documentation describing outbreak definitions was written by Mark Horsman. 
