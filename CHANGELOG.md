# outbreaker Changelog

## Version 0.1.0, 06-10-21

- Initial workflow
- Required inputs: focal sequence list (.txt), COVID-19 reference (.gb),
 master fasta sequences from which to subset (.fa, .fasta)
 - Optional features include output directory, prefix, SNPS only analysis,
 ability to rename headers to custom or match NML specifications,
 and toggling constant sites for SNPs only analysis
 
## Version 0.2.0, 02-11-21
 
 - focal and background filtering step can now be used with --filter,
 where the sequences can be filtered based on genome completeness and
 genome length. The defaults are set to 90% genome completeness and
 a genome length of 29500 for ncov
 
## Version 0.3.0, 15-11-21
 
 - focal and background sequences can now be supplied as either .txt list files 
 of sample names, or as FASTA files containing the actual sequences. outbreaker 
 will assess the file ending and evaluate whether to create subsets based on the 
 names (if .txt is passed) or use the FASTA given
 
## Version 0.4.0, 19-11-21
 - if a previous run of iqtree2 for the SNPs only tree is detected, the console will
 allow the user to select how to proceed. Currently the only possible selection is to confirm
 overwriting the existing SNPs only tree analysis, or outbreaker will exit. Requires a new environment
 installation as the logic uses click through pip. 
 
 
 ## Version 0.5.0, 29-11-21
 - outbreaker now creates an output summary report sumamrizing the number of input sequences, SNP distance patterns relative to the focal sequences inputs, as well as basic rendering of the phylogenetic trees. The report is flexible: it will modify the outputs accordingly if either background sequences are not supplied or SNPs only analysis is not conducted. requires a majoy environment upgrade, specifically with regards to R and Bioconductor dependencies through conda
  

 ## Version 0.6.0, 01-12-21
 - outbreaker now uses snipit to create a graphic of SNP diversity relative to the reference, and includes it in the summary report. This requires an environment upgrade to add snipit through pip
 - The summary report can now handle the recognition of focal and background sequences when samples are renamed through ```--rename```.
 - Still requires teting to verify that ```--rename``` with ```--names_csv``` works in the same way as above
