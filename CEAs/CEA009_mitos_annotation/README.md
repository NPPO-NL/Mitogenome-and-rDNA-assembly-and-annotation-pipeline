Function: executing mitos with multi-fasta files and creating a multi record gbk >
Usage: CEA009_mitos_gbk.py {multi-fasta} {genetic_code} {gbk_output}

Parameter explanation:
{multi-fasta} = A (multi) fasta file that needs to be annotated by MITOS and then converted to a gbk file. 
{genetic_code} = The genetic code refering to the NCBI Genetic codes: https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi. 
Used for determining the translational table to be used by MITOS.
{gbk_output} = Output name of the genbank file

Installation criteria:
Please make sure MITOS is installed with the mitos1-refdata set from the official MITOS github page: https://gitlab.com/Bernt/MITOS.

How to install conda environment:
conda create -n mitos_dev -c bioconda -c conda-forge -c default 'mitos=1.0.5' 'r-base=3.5.1'

Preparation:
1) Make sure that CEA009 and CEA011 are found in the same directory
2) Some line altering in the CEA009_mitos_gbk script and the mitos_gbk bash script are necessary so the script can function in your own environment. 
CEA009_mitos_gbk lines can be found in the script by searching for a "#^" please change these lines according to your own mitos installation folder or temp data directory.  



PLEASE NOTE: 
1) If you want to use this script in CLC Genomics workbench please create an external application and run the mitos_gbk bash script. 
Usage: mitos_gbk_V1.1 {fasta} {translational_table} {gbk-output}
2) CEA011 can be run in the same conda environment as CEA009 since BCBio is installed and BioPython, if BCBio is not installed please install manually in Conda environment.
