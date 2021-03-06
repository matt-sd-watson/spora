# Inputs

spora accepts two modes of arguments that the user may pass: \
    • arguments listed in a config.yaml file as serialized key-value pairs \
    • Individual CLI arguments passed through Python argparse syntax
    
These two modes are mutually exclusive, meaning that if passing arguments through a config.yaml file, ALL of the arguments must be passed in this method. It is also important to note that if a config file is used, and additional arguments are passed as CLI, those arguments will be overwritten by the corresponding arguments written in the config file. Therefore, it is essential that for either mode, all arguments must be passed using the same method.

## Mandatory input formats

Of the arguments passed to spora, the following are required (spora will throw an error if they are not passed in either mode): \
    • ```--focal_sequences```: The collection of target sequences for evaluation by spora (i.e. sequences of interest to the user). These may be passed as either sample names in a .txt file, and spora will parse a master FASTA to retrieve them, or directly as a multi-FASTA file. If passed as a list of names, the format should be as follows:
```
head example_focal_list.txt
seq1
seq2
seq3
seq4
seq5
```
where each line can be replaced with the specific FASTA sample header. Note that the > portion of the FASTA header should NOT be included in the list of names. \
    • ```--reference```: The .gb file used for the alignment step with MAFFT. An example of a compatible COVID-19 reference file can be found in /data/reference/, named **ncov_reference.gb** \
    • ```--master_fasta```: The master FASTA file containing all PHO sequences, from which spora will subset based on input focal and (optional) background lists.
    
Note: that the master_fasta input is required ONLY if either focal_sequences or background_sequences are passed as sample name lists (.txt files). If both are passed as multi-FASTA files (files with an extension of .fa or .fasta), then spora will not require this file to execute. See below for background sequences, as the same formats apply to that input. 

## Optional input formats
The following inputs are purely optional, but may augment the types of analysis that can be conducted using spora: \
    • ```--background_sequences```: The desired collection of context sequences that the user can use to analyze the focal sequences. The format of this input should follow the same rules as focal_sequences (above). \
    
## Sample head renaming

It is common to rename a sample COVID-19 sequence with a different alias for privacy purposes, especially if the outbreak analysis is to be shared with external collaborators. \
spora is designed to facilitate the renaming of FASTA headers to accommodate privacy guidelines and/or to use different label aliases for the outbreak. This feature can be toggled on using ```--rename```. There are two different renaming possibilities for user when ```--rename``` is enabled: \
    • **Option 1**: spora will use the run prefix supplied at runtime to create new alias for each sample. In an example, for a run with 10 samples with run prefix "apartment_can", The new sample names will range from apartment_can_1 to apartment_can_10. A CSV matching the original and newly generated names will be added to the output directory. \
    • **Option 2**: A CSV file of FASTA labels can be supplied using --names_csv. This allows for custom labels for specific samples. Note that not all samples need to have a new name in this CSV. If a sample does not have a coresponding new name, it is left as is as of spora v0.6.4. 
The format of this CSV should be as follows: 
```
original_name     new_name
PHLON21-SARS29115 sequence_1
PHLON21-SARS15665 sequence_2
```

This table will allow spora to use fastafurious to rename the above PHLON sequences with sequence_# headers in all downstream input files generated by the workflow. \
If ```--names_csv``` is supplied, the CSV headers must have original_name for the current/original header name, and new_name for the target/output name to run properly.


## Optional argument descriptions
The following arguments are optional for spora, but may improve and augment the types of analysis and generated files that can be produced from a specific spora run: \
    • ```--output-directory```: If no output directory is specified, spora will attempt to make a new folder named spora in the current directory where the workflow is executed. Furthermore, if the user specifies an output directory that doesn’t yet exist, spora will try to create this path. Therefore, it is important that the user have adequate permissions for the directories that spora will try to access. \
    • ```--prefix```: The prefix denotes a string that will tag each of the output files for a specific spora run. The prefix should be descriptive of the type of analysis being done, or the internal PHO code for the specific outbreak request. If no prefix is supplied by the user, the default is to create each output file with outbreak as the prefix. \
    • ```--filter```: If enabled, the user can also set --genome-completeness and --genome-length to filter out any sequences that do not meet the required thresholds. If --filter is enabled by the other options are not set, then spora will use as default filtering settings genome completeness of 90% as a genome length of 29500. By default, filtering is not enabled. \
    • ```--report```: If enabled, spora will generate a summary report that contains high-level information about the outbreak run and basic analyses (see below). By default, the report is not generated. \
    • ```--snps-only```: By default, spora will conduct routine bioinformatics analyses of the input sequences based on the entire genome. Sometimes, it is beneficial to have phylogenetic analysis conducted using just the variable positions for samples relative to a genome (i.e. consider only the SNP locations for the inputs). if this option is enabled, spora will also create a SNPs-only FASTA file and associated phylogenetic tree in addition to the tree using the entire genome.


### Option 1: config.yaml arguments (Recommended)

An example config.yaml file can be seen below: 

```
focal_list: /home/mwatson/COVID-19/outbreak/example_Oct_2021/focal_names.txt

master_fasta: /home/mwatson/COVID-19/master_fasta/complete_all_12-Oct-2021-09-04.fa

reference: /home/mwatson/COVID-19/reference/reference.gb

outdir: /home/mwatson/COVID-19/outbreak/example_Oct_2021/

snps_only: True

rename: True

prefix: example_Oct_2021
```

For reproducibility, it is recommended to record all arguments in a config.yaml and execute spora with the following command: 

```
spora -c config.yaml
```

### Option 2: CLI argparse arguments

For flexibility, users may also pass CLI arguments to spora. For the config arguments shown above, an equivalent set of CLI arguments to produce the same outputs would be as follows: 

```
spora -f /home/mwatson/COVID-19/outbreak/example_Oct_2021/focal_names.txt \
           -m /home/mwatson/COVID-19/master_fasta/complete_all_12-Oct-2021-09-04.fa \
           -r /home/mwatson/COVID-19/reference/reference.gb \
           -o /home/mwatson/COVID-19/outbreak/example_Oct_2021/ \
           --snps-only \
           --rename \
           -p example_Oct_2021
```

Note that for Boolean arguments such as snps_only or rename, the key value pair in the config.yaml must be set as either True or False, whereas an argparse version passed just detects the presence of the argument. If any of the Boolean arguments is omitted using option #2, then the default behavior is False (to not include). 
In the example above, both the SNPs only analysis and sample renaming features are toggled on by including these arguments in the CLI. Removing them from the command would produce a workflow that does not include them. 


[Next: Outputs](3-OUTPUTS.md)
