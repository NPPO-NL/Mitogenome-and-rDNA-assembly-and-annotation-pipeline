# Mitogenome and rDNA assembly and annotation pipeline
mtDNA and rDNA assembly and annotation pipeline

We created an Illumina sequencing pipeline in CLC genomics workbench for the assembly and annotation of (near complete) rDNA and mtDNA sequences containing the 18S, 28S and cox1 barcodes for nematode identification. 


This repository is created for sharing scripts and environments related to the Mitogenome and rDNA assembly and annotation pipeline.
The mtDNA and rDNA assembly and annotation pipeline is built in CLC Genomics Workbench. Therefore, not all modules are self written scripts. 
The scripts that were developed for this project, the so called CLC External Applications (CEAs) are included in this repository.
More information on CEAs can be found on: https://github.com/NPPO-NL/CLC-External-Applications.
The CEAs used for creating the Mitogenome and rDNA assembly and annotation pipeline are:
	CEA001_BLASTn
	CEA004_Select_sequences_based_on_BLAST_hits
	CEA005_Krona 
	CEA009_mitos_annotation
	CEA010_barrnap_annotation
	CEA011_gff_to_gbk

The .xml files found in this repository are CLC External Application files which can be imported and contain the command used for running the CEA.


Please note: 
CEA001 calls upon no Python script, but calls upon the BLAST+ program which can be downloaded from: https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/
CEA005 calls upon no Python script, but calls upon the KronaTools program, which can be downloaded from: https://github.com/marbl/Krona/tree/master/KronaTools
Make sure that all installation criteria are met for all CEAs. 
