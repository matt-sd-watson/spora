from spora.config import *
import os
import sys
import yaml

def get_defaults():

    default_dict = {
        # all spora input options
        KEY_FOCAL_SEQS: "",
        KEY_BACKGROUND_SEQS: "",
        KEY_OUTDIR: "",
        KEY_REFERENCE: "",
        KEY_MASTER_FASTA: "",
        KEY_THREADS: 2,
        KEY_SNPS_ONLY: False,
        KEY_RENAME: False,
        KEY_NAMES_CSV: "",
        KEY_PREFIX: "outbreak",
        KEY_CONST_SITES: True,
        KEY_FILTER: False,
        KEY_GENOME_COMPLETENESS: 90,
        KEY_GENOME_LENGTH: 29500,
        KEY_REPORT: False
    }
    return default_dict

def valid_inputs(config):

    valid_arguments = {
    "focal_seqs": "focal_seqs",
    "background_seqs": "background_seqs",
    "outdir": "outdir",
    "reference": "reference",
    "nthreads": "nthreads",
    "snps_only": "snps_only",
    "rename": "rename",
    "names_csv": "names_csv",
    "prefix": "prefix",
    "const_sites": "const_sites",
    "filter": "filter",
    "genome_completeness": "genome_completeness",
    "genome_filter": "genome_filter",
    "report": "report"}

    for i in config:
        valid_arguments[i] = i

    return valid_arguments


def check_configfile(cwd, config_arg):
    configfile = os.path.join(cwd, config_arg)

    # ending = configfile.split(".")[-1]

    # if ending not in ["yaml", "yml"]:
        #sys.stderr.write(f'Error: config file {configfile} must be in yaml format.\n')
        #sys.exit(-1)

    if not os.path.isfile(configfile):
        sys.stderr.write(f'Error: cannot find config file at {configfile}\n')
        sys.exit(-1)
    else:
        print(f"Input config file detected: {configfile}")
        return configfile

def load_yaml(f):
    try:
        input_config = yaml.load(f, Loader=yaml.FullLoader)
    except:
        sys.stderr.write(f'Error: failed to read config file. Ensure your file in correct yaml format.\n')
        sys.exit(-1)
    return input_config

def setup_absolute_paths(path_to_file,value):
    return os.path.join(path_to_file,value)

def return_path_keys():
    return[KEY_FOCAL_SEQS,
           KEY_BACKGROUND_SEQS,
           KEY_REFERENCE,
           KEY_NAMES_CSV,
           KEY_MASTER_FASTA]

def parse_yaml_file(configfile, configdict):
    path_keys = return_path_keys()

    path_to_file = os.path.abspath(os.path.dirname(configfile))

    valid_keys = valid_inputs(configdict)

    invalid_keys = []

    with open(configfile, "r") as f:
        input_config = load_yaml(f)  # try load file else exit with msg

        valid_keys = valid_inputs(configdict)
        for key in input_config:
            value = input_config[key]
            if value is None:  # dont count blank entries
                pass
            else:
                clean_key = key.lstrip("-").replace("-", "_").rstrip(" ").lstrip(" ").lower()

                if clean_key in valid_keys:
                    clean_key = valid_keys[clean_key]
                else:
                    invalid_keys.append(key)
                    break

                if clean_key in path_keys:
                    value = setup_absolute_paths(path_to_file, value)
                configdict[valid_keys[clean_key]] = value


    if len(invalid_keys) == 1:
        print(f'Error: invalid key in config file.\n')
        sys.exit(-1)
    elif len(invalid_keys) > 1:
        keys = ""
        for i in invalid_keys:
            keys += f"\t- {i}\n"
        print(f'Error: invalid keys in config file.\n')
        sys.exit(-1)



def setup_config_dict(cwd, config_arg):
    config = get_defaults()

    if config_arg:
        configfile = check_configfile(cwd, config_arg)
        parse_yaml_file(configfile, config)
    else:
        print("There was an error in parsing the input config file")
        sys.exit(-1)

    return config


