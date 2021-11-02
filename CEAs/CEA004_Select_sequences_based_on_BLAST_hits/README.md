# CEA004_Select_chunks_without_hits

This script is written for Python 3.x
This script reads a BLASTn result en the multi-fasta that was used for BLASTn, extracts the sequences without BLASTn hit and writes this in a new multi-fasta file.

required packages: sys, getopt, re, biopython

parameters:
inputfile1: Path to BLASTn table, inputfile2: Path to .fasta, outputfile: Path to output

While in the directory of the script:
./CEA003_chunk_ file_v2.1.py -b <inputfile1> -c <inputfile2> -o <outputfile>
