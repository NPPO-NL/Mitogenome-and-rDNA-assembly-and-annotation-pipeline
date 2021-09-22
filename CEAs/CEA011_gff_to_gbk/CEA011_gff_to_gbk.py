#!/usr/bin/env python2


"""
Developer: Thijn van Kempen
Function: Convert a GFF and associated FASTA file into GenBank format.
Usage:
    CEA011_gff_to_gbk.py <FASTA sequence file> <GFF annotation file> <output>

Code adapted from: https://github.com/chapmanb/bcbb/blob/master/gff/Scripts/gff/gff_to_genbank.py
Commented on: 12-01-2021
"""

from __future__ import print_function

import sys
import os
import argparse
from Bio import SeqIO
from Bio.Alphabet import generic_dna
from Bio import Seq
from BCBio import GFF
import re


def main():
    """
    Main function of the script
    :return:
    """

    #parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("fasta", help="Fasta input")
    parser.add_argument("gff", help="GFF input")
    parser.add_argument("output", help="Genbank output directory")
    args = parser.parse_args()
    fasta_file = args.fasta
    gff_file = args.gff
    out_file = args.output
    #out_file = args.output + ".gb"

    #function calling
    fasta_input = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta", generic_dna))
    gff_iter = GFF.parse(gff_file, fasta_input)
    SeqIO.write(_check_gff(_fix_ncbi_id(gff_iter)), out_file, "genbank")


def _fix_ncbi_id(fasta_iter):
    """
    Fixing the ncbi identifier format.
    :param fasta_iter: Fasta iteration.
    :return:
    """

    """GenBank identifiers can only be 16 characters; try to shorten NCBI.
    """
    prog = re.compile("contig_[0-9]*")
    for rec in fasta_iter:
        old_rec_name = rec.name

        result = prog.search(old_rec_name)
        if result:
            rec.id = result.group(0)
            rec.name = result.group(0)
        elif len(old_rec_name) > 16:
            if old_rec_name.find("|") > 0:
                new_id = [x for x in old_rec_name.split("|") if x][0][:16]
                print("Warning: shortening NCBI name %s to %s" % (rec.id, new_id))
                rec.id = new_id
                rec.name = new_id
            if old_rec_name.find("_") > 0:
                new_id = [x for x in old_rec_name.split("_") if x][0][:16]
                print("Warning: shortening NCBI name %s to %s" % (rec.id, new_id))
                rec.id = new_id
                rec.name = new_id

        old_rec_name = ""
        yield rec


def _check_gff(gff_iterator):
    """
    Checks if the file is a gff file.
    :param gff_iterator: gff file
    :return:
    """

    """Check GFF files before feeding to SeqIO to be sure they have sequences.
    """
    for rec in gff_iterator:
        if isinstance(rec.seq, Seq.UnknownSeq):
            print("Warning: FASTA sequence not found for '%s' in GFF file" % (
                    rec.id))
            rec.seq.alphabet = generic_dna
        yield _flatten_features(rec)


def _flatten_features(rec):
    """

    :param rec: gff record
    :return: returns flattend gff record
    """


    """Make sub_features in an input rec flat for output.

    GenBank does not handle nested features, so we want to make
    everything top level.
    """
    out = []
    for f in rec.features:
        cur = [f]
        while len(cur) > 0:
            nextf = []
            for curf in cur:
                out.append(curf)
                if len(curf.sub_features) > 0:
                    nextf.extend(curf.sub_features)
            cur = nextf
    rec.features = out
    return rec


if __name__ == "__main__":
    main()
