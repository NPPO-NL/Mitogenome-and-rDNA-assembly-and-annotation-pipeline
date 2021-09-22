#!/usr/bin/env python


"""
Code written by: Thijn van Kempen and assisted by Lucas van der Gouw
Function: executing mitos with multi-fasta files and creating a multi record gbk result file.
Finished and commented on: 12-01-2021

Usage: CEA009_mitos_gbk.py {multi-fasta} {genetic_code} {gbk_output}
"""

#All imports
import os
import shutil
import argparse
from Bio import SeqIO
import glob



def main():
    """
    Main function of the script
    :return:
    """

    #MAKE SURE ALL DIRECTORIES BELOW ARE AVAILABLE AND ACCESSIBLE
    base_dir = "/home/molbio/"
    tmp_files = base_dir + "CEA009_tmp/"
    fasta_dir = base_dir + "CEA009_tmp/fasta/"
    gff_dir =  base_dir + "CEA009_tmp/gff/"
    mitos_out = base_dir + "CEA009_tmp/mitos/"
    tmp_output_paths = [tmp_files, fasta_dir, gff_dir, mitos_out]
    script_loc = "/MolbioDataDrive/Scripts/"
    #Change two paths below to install folder of mitos and reference set
    mitos_path = "/opt/MITOS/"
    mitos_ref = mitos_path + "data/mitos1-refdata/"


    #Parser handling
    parser = argparse.ArgumentParser()
    parser.add_argument("fasta", help="Fasta input file")
    parser.add_argument("genetic_code", help="Genetic code")
    parser.add_argument("output", help="Gbk output file")
    #parser.add_argument("fasta_out", help="Corrected multi-fasta")
    args = parser.parse_args()
    fasta_file = args.fasta
    genetic_code = args.genetic_code
    output = args.output
    gff_out = args.output + ".gff"
    fasta_out = args.output + ".fasta"

    #Function calling
    remove_tmp(tmp_files)
    dir_creator(tmp_output_paths)
    fasta_splitter(fasta_file, fasta_dir, fasta_out)
    run_mitos(fasta_dir, gff_dir, mitos_out, mitos_path,
              mitos_ref, genetic_code)
    gff_merger(gff_dir, gff_out)
    make_gbk(fasta_out, gff_out, output, script_loc)
    remove_tmp(tmp_files)


def dir_creator(path_list):
    """
    Create directories if non existing.
    :param path_list:
    :return:
    """
    for file_path in path_list:
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)


def fasta_splitter(fasta_input, fasta_out, cor_multi_fas):
    """

    :param fasta_input: The multi fasta input file
    :param fasta_out: The splitted fasta output file.
    :return:
    """
    with open(cor_multi_fas,'w') as multi_out:

        for seq_record in SeqIO.parse(fasta_input, "fasta"):
            #removing "(" and ")" from fasta header, not compatible with mitos
            new_id = seq_record.id.replace("(","").replace(")","")
            fasta_output = fasta_out + str(new_id + ".fa")
            multi_out.write(">" + str(new_id) + "\n" + str(seq_record.seq) + "\n")
            with open(fasta_output, 'w') as output:
                output.write(">" + str(new_id) + "\n" + str(seq_record.seq))


def run_mitos(fasta_folder, gff_folder, mitos_output, mitos_install, reference, genetic_table):
    """

    :param fasta_folder: Location where fasta records are stored
    :param gff_folder: Location where gff records are stored
    :param mitos_output: Location where mitos output are generated
    :param mitos_install: Location where mitos is installed
    :param reference: Location of the mitos reference set
    :param genetic_table: Genetic code (see mitos website)
    :return:
    """
    #MAKE SURE MITOS CAN BE FOUND IN /opt/MITOS/
    counter = 0
    fasta_total = len(glob.glob(os.path.join(fasta_folder, '*.fa')))
    for fasta in glob.glob(os.path.join(fasta_folder, '*.fa')):
        counter += 1
        print("Start mitos execution {} out of {}".format(counter, fasta_total))
        os.system("{}runmitos.py -i {} -c {} -o {} -r {}".format(mitos_install, fasta, genetic_table, mitos_output, reference))
        gff_copy(counter, mitos_output, gff_folder)
	remove_tmp(mitos_output)
	dir_creator([mitos_output])


def gff_copy(result_number, mitos_dir, gff_dir):
    """
    Copies gff file from MITOS output dir to non temporary location
    :param result_number: Number indicating the -nth gff file.
    :param mitos_dir: Location where mitos is installed
    :param gff_dir: Location where gffs are stored.
    :return:
    """
    print("Moving to output dir to extract gff")
    cwd = os.getcwd()
    os.chdir("{}".format(mitos_dir))
    print("Copying result.gff to tmp_folder")
    os.system("cp {}result.gff {}result{}.gff".format(mitos_dir, gff_dir, str(result_number)))
    print("Returning to script working dir")
    os.chdir(cwd)


def gff_merger(gff_folder, gff_out):
    """
    Merges all copied gffs into one multi gff entry.
    :param gff_folder: Folder where all the gffs are stored
    :param gff_out: The merged gff file
    :return:
    """
    with open(gff_out, "w") as output:
        for gff in glob.glob(os.path.join(gff_folder, '*.gff')):
            with open(gff, "r") as input:
                output.write(input.read())


def make_gbk(fasta, gff, gbk, script_dir):
    """
    Running CEA011 that allows to convert the created gff and fasta into a gbk format
    :param fasta: fasta input file
    :param gff: gff input file
    :param gbk: gbk output file
    :return:
    """
    cwd = os.getcwd()
    os.system("python {}CEA011_gff_to_gbk.py {} {} {}".format(script_dir, fasta, gff, gbk))
    os.chdir(cwd)


def remove_tmp(folder):
    """
    Code for deleting a folder and sub folder as well as its contents.
    Code adapted from: https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder
    :param folder: The path of the folder that can be removed (temporary folder)
    :return:
    """

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    #Remove all gffs and mitos output


if __name__ == "__main__":
    main()
