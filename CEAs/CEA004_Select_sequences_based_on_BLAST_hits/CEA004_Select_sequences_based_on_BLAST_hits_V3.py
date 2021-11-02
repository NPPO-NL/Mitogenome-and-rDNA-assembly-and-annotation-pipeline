#!/usr/bin/env python
"""
Created on Mon Apr 24 13:43:32 2017

@author: Lucas v.d. Gouw
Updated: 08-01-2021 By: Thijn van Kempen
This script reads a BLASTn result and the multi-fasta that was used for BLASTn, 
extracts the sequences without BLASTn hit and writes this in a new multi-fasta file.

New in V3:
Script also allows the BLASTx result input. 
Also gives the user the option to extract sequences from BLAST hits. 
Usage: CEA004_Selected_sequences_based_on_BLAST_hits_V3.py
{blast_table} {fasta_input} {fasta_output} {blast_switch} {hits_switch}
"""


"""
To be updated: Make dummy fasta file if fasta output is completely empty

"""

import sys, getopt, re, argparse
from Bio import SeqIO

# ensure correct command-line opperation. 
# -b expects the BLAST result, -c expects the multi-fasa used in BLASTn and -o expects the filename for multi-fasta output
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("blast_table", help="") #update
    parser.add_argument("fasta_input", help="Fasta input file")
    parser.add_argument("fasta_output", help="Fasta output")
    parser.add_argument("blast_switch", help="For BLASTn use 'n' for BLASTx use 'x'") #update
    parser.add_argument("hits_switch", help="For hits sequences use '1' for non hit sequences use '0'") #update
    args = parser.parse_args()
    blast_table = args.blast_table
    fasta_input = args.fasta_input
    fasta_output = args.fasta_output
    blast_switch = args.blast_switch
    hits_switch = args.hits_switch

    open_blast_table = open_files(blast_table)
    open_fasta_input = open_files(fasta_input)
    if blast_switch == "BLASTn":
        sequence_list = add_sequences_blastn(open_blast_table, hits_switch)
        processSequences(sequence_list, open_fasta_input, fasta_output)
    if blast_switch == "BLASTx":
        sequence_list = add_sequences_blastx(open_blast_table, open_fasta_input, hits_switch)
        open_fasta_input = open_files(fasta_input)
        processSequences(sequence_list, open_fasta_input, fasta_output)



# read the BLASTn result and multi-fasta
def open_files(inputfile1):
    read_file1 = open(inputfile1,"r")


    return read_file1

# add BLASTn file to string, use regular expressions to find sequences with 0 hits
# find the sequence names and add the sequences to a string
def add_sequences_blastn(blast_table, hits_check):
    non_hit_sequences = set()
    hit_sequences = set()
    blast_file =""
    counter = 0
    for line in blast_table:
        blast_file += line
    blast_table.close()
    matches = re.findall('Query: .*', blast_file)
    hits = re.findall('\d* hits', blast_file)
    for match in matches:
        match = match.replace("Query: ","")
        #match = match.replace("(","").replace(")","")
        hitnumber = hits[counter]
        counter += 1
        print(match)
        hitnumber = hitnumber.replace(" hits","")
        if hitnumber == "0":
            non_hit_sequences.add(str(match))
        if hitnumber != "0":
            hit_sequences.add(str(match))

    if hits_check == "hits":
        return hit_sequences

    if hits_check == "no_hits":
        return non_hit_sequences


def add_sequences_blastx(blast_table, fasta_input, hits_check):
    all_fasta_ids = set()
    for s in SeqIO.parse(fasta_input, "fasta"):
        #print(s)
        all_fasta_ids.add(s.id)


    blastx_ids = set()


    for line in blast_table:
        fasta_blast_id = line.split("\t")[0]
        #fasta_blast_id = fasta_blast_id.replace("(","").replace(")","")
        blastx_ids.add(fasta_blast_id)

    no_hits = all_fasta_ids - blastx_ids
    yes_hits = blastx_ids

    #print(no_hits)

    if hits_check == "hits":
        return yes_hits

    if hits_check == "no_hits":
        #print(no_hits)
        return no_hits


def processSequences(sequences, sequenceFile, outfile):
    new =[]
    print(sequences)
    for s in SeqIO.parse(sequenceFile, "fasta"):
#        print(s)
        if s.id in sequences:
            #s.id = s.id.replace("(","").replace(")","")
            new.append(s)
    #print(new)
    SeqIO.write(new, outfile, "fasta")


if __name__ == "__main__":
   main()
