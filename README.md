# outbreaker

snakemake and Python integrated workflow for intermediate file generation for COVID outbreak analysis

## installation

```
git clone https://github.com/matt-sd-watson/ncov_outbreaker.git
conda env create -f ncov_outbreaker/environments/environment.yml
conda activate ncov_outbreaker
cd outbreaker
pip install . 
```

## usage
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
  -f FOCAL_LIST, --focal-list FOCAL_LIST
                        Input .txt list of focal sample names for outbreak
  -b BACKGROUND_LIST, --background-list BACKGROUND_LIST
                        Optional input .txt list of background sample names to add to analysis
  -m MASTER_FASTA, --master-fasta MASTER_FASTA
                        Master fasta of COVID sequences to select from
  -o OUTDIR, --output-directory OUTDIR
                        Path to the desired output directory
  -r REFERENCE, --reference REFERENCE
                        .gb file containing the desired COVID-19 reference sequence
  -p PREFIX, --prefix PREFIX
                        Prefix string to label all output files. Default: outbreak
  -n NTHREADS, --nthreads NTHREADS
                        Number of threads to use for processing. Default; 4
  -s, --snps-only       Generate a snps-only FASTA from the input FASTA. Default: False
  -rn, --rename         Rename the FASTA headers to be compatible with NML standards. Default: False
  -nc NAMES_CSV, --names-csv NAMES_CSV
                        Use the contents of a CSV to rename the input FASTA. requires the following column headers: original_name, new_name
  -ncs, --no-constant-sites
                        Do not enable constant sites to be used for SNPs only tree generation. Default: Enabled
```
