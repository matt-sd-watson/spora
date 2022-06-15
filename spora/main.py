from spora import __version__
import spora.init_defaults as defaults

import os
import sys
import argparse
import snakemake
import yaml

cwd = os.getcwd()
thisdir = os.path.abspath(os.path.dirname(__file__))


def isFasta(input):
    return input.endswith(('.fa', '.fasta', '.FA', '.FASTA'))

# set mandatory input args from either config or CLI
# mandatory = set(["focal_list", "reference", "master_fasta"])

def get_primary_snakefile(thisdir):
    snakefile = os.path.join(thisdir, 'workflows', 'spora.smk')
    if not os.path.exists(snakefile):
        print(f'Error: cannot find Snakefile at {snakefile}\n Check installation\n')
        sys.exit(-1)
    return snakefile


def main(sysargs = sys.argv[1:]):
    parser = argparse.ArgumentParser(add_help=False,
                                    description="spora: Streamlined Phylogenomic Outbreak Report Analysis",
                                    usage='''
    \tspora -c <config.yaml> 
    \tOR
    \tspora --focal_list ...<input args>''')

    parser.add_argument('-h', "--help", action="help",
                        help="Show the help output and exit.",
                        dest="help")

    parser.add_argument('-c', "--config", action="store",
                         help="Input config file in yaml format, all command line arguments can be passed via the config file.",
                         dest="config")

    parser.add_argument('-f', "--focal-sequences", action="store",
                        help="Input .txt list or multi-FASTA focal samples for outbreak. Required",
                        dest="focal_seqs", default="")

    parser.add_argument('-b', "--background-sequences", action="store",
                        help="Optional input .txt list or multi-FASTA background samples to add to analysis",
                        dest="background_seqs", default="")

    parser.add_argument('-m', "--master-fasta", action="store",
                        help="Master FASTA of genomic sequences to select from. Required if either --focal-sequences "
                             "or --background-sequences are not supplied in FASTA format",
                        dest="master_fasta", default="")

    parser.add_argument('-o', "--output-directory", action="store",
                        help="Path to the desired output directory. If none is provided, "
                             "a new folder named spora will be created in the current directory",
                        dest="outdir", default="")

    parser.add_argument('-r', "--reference", action="store",
                        help=".gb file containing the desired COVID-19 reference sequence. Required",
                        dest="reference", default="")

    parser.add_argument('-p', "--prefix", action="store",
                        help="Prefix string to label all output files. Default: outbreak",
                        dest="prefix", default="outbreak")

    parser.add_argument('-t', "--nthreads", action="store",
                        help="Number of threads to use for processing. Default: 2",
                        dest="nthreads", default=2, type=int)

    parser.add_argument('-s', "--snps-only", action="store_true",
                        help="Generate a snps-only FASTA from the input FASTA. Default: False",
                        dest="snps_only")

    parser.add_argument('-rn', "--rename", action="store_true",
                        help="Rename the FASTA headers to be compatible with NML standards. Default: False",
                        dest="rename")

    parser.add_argument('-nc', "--names-csv", action="store",
                        help="Use the contents of a CSV to rename the input FASTA. Requires the following "
                             "column headers: original_name, new_name",
                        dest="names_csv", default="")

    parser.add_argument('-ncs', "--no-constant-sites", action="store_false",
                        help="Do not enable constant sites to be used for SNPs only tree generation. Default: Enabled",
                        dest="const_sites")

    parser.add_argument('-fi', "--filter", action="store_true",
                        help="Filter both the focal and background sequences based on genome "
                             "completeness and length. Default: Not enabled",
                        dest="filter")

    parser.add_argument('-gc', "--genome-completeness", action="store",
                        help="Integer for the minimum genome completeness percentage for filtering. Default: 90",
                        dest="genome_completeness", default=90, type=int)
    parser.add_argument('-gl', "--genome-length", action="store",
                        help="Integer for the minimum genome length for filtering. Default: 29500",
                        dest="genome_length", default=29500, type=int)

    parser.add_argument('-rp', "--report", action="store_true",
                        help="Generate a summary output report for the spora run. Default: Not enabled",
                        dest="report")

    parser.add_argument('-v', "--version", action="version",
                        help="Show the current spora version then exit.",
                        version=f"This is spora: v{__version__}")



    if len(sysargs) < 1:
        parser.print_help()
        sys.exit(0)
    else:
        args = parser.parse_args(sysargs)

    if args.config:
        # if args are passed in a config file, they overwrite any existing args or others passed by CLI

        all_valid_inputs = True
        with open(args.config, "r") as f:
            args_to_dict = defaults.load_yaml(f)

        config = defaults.setup_config_dict(cwd, args.config)

        if isFasta(str(config["focal_seqs"])):
            # if both focal and background are fasta, no need for master file
            if config["background_seqs"] == '' or isFasta(str(config["background_seqs"])):
                mandatory = set(["focal_seqs", "reference"])
            # if focal is fasta but background is not, keep master file
            elif config["background_seqs"] != '' or not isFasta(str(config["background_seqs"])):
                mandatory = set(["focal_seqs", "reference", "master_fasta"])
        else:
            mandatory = set(["focal_seqs", "reference", "master_fasta"])

        current_keys = set([key for key in args_to_dict])
        if len(current_keys.intersection(mandatory)) != len(mandatory):
            sys.stderr.write(f'One of more required parameters were not passed in the config:\n{mandatory}\n')
            sys.exit(-1)

        all_valid_inputs = True
        for key in args_to_dict:
            if args_to_dict[key] == "" or args_to_dict[key] is None and key in mandatory:
                all_valid_inputs = False
                sys.stderr.write(f'The following config parameter was passed as empty. It is required: {key}\n')

        if not all_valid_inputs:
            sys.stderr.write(f'ERROR: Please review the config inputs\n')
            sys.exit(-1)

    else:
        # if the args are not passed in a config file, create a config dictionary for snakemake
        config = vars(args)

        if isFasta(str(config["focal_seqs"])):
            # if both focal and background are fasta, no need for master file
            if config["background_seqs"] == '' or isFasta(str(config["background_seqs"])):
                mandatory = set(["focal_seqs", "reference"])
            # if focal is fasta but background is not, keep master file
            elif config["background_seqs"] != '' or not isFasta(str(config["background_seqs"])):
                mandatory = set(["focal_seqs", "reference", "master_fasta"])
        else:
            mandatory = set(["focal_seqs", "reference", "master_fasta"])

        all_valid_inputs = True
        for key in config.keys():
            # If the mandatory key is not passed on the CLI, flag and exit
            if config[key] == '' and key in mandatory:
                all_valid_inputs = False
                sys.stderr.write(f'The following CLI parameter was not passed. It is required: {key}\n')

        if not all_valid_inputs:
            sys.stderr.write(f'ERROR: Please review the command line inputs\n')
            sys.exit(-1)

    snake_file = get_primary_snakefile(thisdir)

    status = snakemake.snakemake(snake_file, printshellcmds=True, forceall=True, force_incomplete=True,
                                 config=config, cores=args.nthreads, lock=False, quiet = True
                                 )

    if status:  # translate "success" into shell exit code of 0
        sys.stderr.write(f"\nspora completed successfully.\n")
        return 0

    sys.stderr.write(f"\nspora did not complete successfully.\n")
    return 1

if __name__ == '__main__':
    main()
