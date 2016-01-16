#!/usr/bin/python

import PyPDF2
import argparse
import os

__author__ = 'Luca Doglione'


class PdfMerger:
    @staticmethod
    def merge_sequential(output, verbose, names, pdf):
        merge = PyPDF2.PdfFileMerger()
        index = 0
        for p in pdf:
            if verbose:
                print "-> [Merging]Append File {}".format(names[index])
            index += 1
            merge.append(p)

        if verbose:
            print "-> Writing Output file {}".format(output)

        try:
            merge.write(file(output, 'wb'))
        except IOError as e:
            print "*** The Script have encountered an error writing output file {}: {}".format(output, e.strerror)
            exit()

    @staticmethod
    def merge_alternate(output, verbose, names, pdf):
        out = PyPDF2.PdfFileWriter()

        # Calculate max number of pages
        if verbose:
            print "-> Calculate max number of pages"

        max_p = 0
        for p in pdf:
            if p.getNumPages() > max_p:
                max_p = p.getNumPages()

        if verbose:
            print "-> Max number of pages is {}".format(max_p)

        # Start Merging
        for i in range(0, max_p):
            index = 0
            for f in pdf:
                if f.getNumPages() >= i + 1:
                    if verbose:
                        print "-> [Merging]Take page {} from file {}".format(i, names[index])
                    page = f.getPage(i)
                    out.addPage(page)
                elif verbose:
                    print "-> [Merging]No more pages from file {}".format(names[index])
                index += 1

        # Make Output
        try:
            out.write(file(output, 'wb'))
        except IOError as e:
            print "*** The Script have encountered an error writing output file {}: {}".format(output, e.strerror)
            exit()

    @staticmethod
    def main(**args):
        # Print of initial Message
        if not args['quiet']:
            if args['alternate']:
                print "Merging {} PDF files with alternate method".format(len(args['fileNames'])+1)
            else:
                print "Merging {} PDF files with sequential method".format(len(args['fileNames'])+1)
            print "Retrieving Files..."

        if args['reverse'] is not None:
            if not args['quiet']:
                print "Reversing specified files..."
            for i in args['reverse']:
                PdfMerger.reverse(args['fileNames'][i], args['fileNames'][i]+'rev', args['verbose'])
                args['fileNames'][i] += 'rev'

        name = ""
        pdf_files = []
        pdf_names = []
        try:
            # Init structure tu memorize pdf open files
            if args['verbose']:
                print "-> Init Data Structure"

            # Open and Append First File
            name = args['firstFile']
            if args['verbose']:
                print "-> Open File {}".format(name)
            f = PyPDF2.PdfFileReader(file(name, 'rb'))
            pdf_files.append(f)
            pdf_names.append(name)

            # Open and Append others Files
            for name in args['fileNames']:
                if args['verbose']:
                    print "-> Open File {}".format(name)
                f = PyPDF2.PdfFileReader(file(name, 'rb'))
                pdf_files.append(f)
                pdf_names.append(name)

        except IOError as e:
            print "*** The Script have encountered an error opening file {}: {}".format(name, e.strerror)
            exit()

        if not args['quiet']:
            print "Files Retrieved, Start Merging..."

        output_name = args['output']

        if args['sequential']:
            PdfMerger.merge_sequential(output_name, args['verbose'], pdf_names, pdf_files)
        else:
            PdfMerger.merge_alternate(output_name, args['verbose'], pdf_names, pdf_files)

        if args['reverse'] is not None:
            if not args['quiet']:
                print "Remove temporary files"
            for i in args['reverse']:
                if args['verbose']:
                    print "-> Removing temporary file {}".format(args['fileNames'][i])
                os.remove(args['fileNames'][i])

        if not args['quiet']:
            print "Files Merged successfully in a new PDF file: {}".format(output_name)

    @staticmethod
    def reverse(name, output, verbose):

        if verbose:
            print "Reverse of File: {}".format(name)

        f = file(name, 'rb')
        pdf_in = PyPDF2.PdfFileReader(f)
        pdf_o = PyPDF2.PdfFileWriter()

        # Calculate Number of Page of the file
        n = pdf_in.getNumPages()
        if verbose:
            print "-> Start reversing File {} in {}: {} pages".format(name, output, n)

        # Reversing File
        for i in range(0, n):
            if verbose:
                print "-> [Reversing] take page {} from file {}".format(n-i, name)
            page = pdf_in.getPage(n-1-i)
            pdf_o.addPage(page)

        o = file(output, 'wb')

        # Make Output
        try:
            pdf_o.write(o)
        except IOError as e:
            print "*** The Script have encountered an error writing output file {}: {}".format(output, e.strerror)
            exit()
        finally:
            o.close()

        if verbose:
            print "-> File {} reversed in {}".format(name, output)


# Start point for script
if __name__ == "__main__":

    # Description of the script
    script_desc = "Script that merge PDF files in an output files." +\
                  "There are two different method: Sequential (default) and Alternate:"

    # Declaration of parser for arguments
    parser = argparse.ArgumentParser(description=script_desc)

    # Declaration of positional Arguments
    parser.add_argument('firstFile', help='First file to be merged')
    parser.add_argument('fileNames', metavar='otherFile', nargs='+',
                        help='Other pdf Files that have to be merged with first')

    # Declaration of a Mutual Exclusive group of optional Arguments for Merging Algorithm
    mergingAlg = parser.add_mutually_exclusive_group()
    mergingAlg.add_argument('-s', '--sequential', action='store_true', default=False,
                            help='Sequential method, files will be merged in the same order as user specified them')
    mergingAlg.add_argument('-a', '--alternate', action='store_true', default=False,
                            help="Alternate method, files will be merged taking one page from each file at a time")

    # Declaration of optional Arguments
    parser.add_argument('-o', '--output', default="MergedFile.pdf",
                        help="FileName for the output file")
    parser.add_argument('-r', '--reverse', metavar='i', nargs='+', type=int,
                        help='Select index of otherFile that have to be reversed before merging')

    # Declaration of a Mutual Exclusive group of optional Arguments for Output Mode
    outputMode = parser.add_mutually_exclusive_group()
    outputMode.add_argument('-q', '--quiet', action='store_true', default=False,
                            help='Set a Quiet Output for the Script')
    outputMode.add_argument('-v', '--verbose', action='store_true', default=False,
                            help='Set a Verbose Output for the Script')

    args_list = parser.parse_args()

    if not args_list.sequential and not args_list.alternate:
        args_list.sequential = True

    if args_list.reverse is not None:
        if max(args_list.reverse) > len(args_list.fileNames) - 1:
            print "*** ERROR: specified index for reversing is out of range"
            exit()

    PdfMerger().main(**vars(args_list))
