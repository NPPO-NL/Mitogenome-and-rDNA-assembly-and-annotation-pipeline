#!/usr/bin/env python


"""
Name: Thijn van Kempen
Function: Annotate rDNA sequences with Barrnap
First line written: 30/09/2020
Release date: 05/11/2020
"""

import os
import argparse


def main():
    """
    The main function of the script.

    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Fasta rDNA input")
    parser.add_argument("output", help="GFF annotation")
    parser.add_argument("kingdom", help="Choose kingdom")
    args = parser.parse_args()
    command(args)


def command(arguments):
    """
    Execute a command on the command line
    arguments: the arguments passed on by calling the script
    :return:
    """
    os.system("barrnap --kingdom {} {} > {}".format(arguments.kingdom, arguments.input, arguments.output))


if __name__ == "__main__":
    main()
