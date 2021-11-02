<h1>CEA004_Select_sequences_based_on_BLAST_hits</h1>

This script is written for Python 3.x
This script reads a BLASTn or BLASTx result table and the multi-fasta that was used for that BLAST result table and extracts the sequences with or without BLASTn/x hit and writes this in a new multi-fasta file.

required packages: sys, getopt, re, biopython

Parameter explanation:
{blast_table} = the BLAST hit input table. 
{fasta_input} = the (multi-record) FASTA input file
{fasta_output} = the new FASTA file containing the hit or non hit sequences
{blast_switch} = Define the type of BLAST result table here, for BLASTn use 'n', for BLASTx use 'x'
{hits_switch} = For retrieving hits sequences use '1', for retrieving non hit sequences use '0'

While in the directory of the script:
./CEA004_Select_sequences_based_on_BLAST_hits_V3.py {blast_table} {fasta_input} {fasta_output} {blast_switch} {hits_switch}
