Function: Convert a GFF and associated FASTA file into GenBank format.
Usage:
    CEA011_gff_to_gbk.py <FASTA sequence file> <GFF annotation file> <output>

Parameter explanation:
<FASTA sequence file> = (Multi-)Fasta sequence file containing the sequences that you want to convert to a gbk.
<GFF annotation file> = Gene Feature Format file with annotation information belonging to the input fasta sequences. 
<output> = Output name of the genbank file

Please make sure that you have the following installed:
Python2 with BioPython and BCBio


Please note that the code is adapted from: 
https://github.com/chapmanb/bcbb/blob/master/gff/Scripts/gff/gff_to_genbank.py
