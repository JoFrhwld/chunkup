from pysox import CSoxApp
import argparse
import re
import string
import csv
import os


class NamingException(Exception):
    '''An exception for chunk naming problems'''
    pass

class DirectoryException(Exception):
    '''Problem with output directory'''
    pass

def check_outdir(outdir):
    '''Checks to see if there is an output directory'''
    if not os.path.exists(outdir):
        raise DirectoryException("No such directory %s"%outdir)
    elif not os.path.isdir(outdir):
        raise DirectoryException("%s is not a directory"%outdir)

def chunk_audio(audio, outfile, start_time, end_time):
    '''Sets up sox to trim the audio'''
    sapp = CSoxApp(audio, output = outfile, 
                   effectparams = [('trim', [start_time, end_time])])
    sapp.flow()

def make_chunkname(variables, config_string, name_dict):
    '''make chunk name'''
    chunk_name = config_string
    for var in variables:
        if var not in name_dict:
            raise NamingException("%s not found"%var)

        chunk_name = chunk_name.replace(var, str(name_dict[var]))
    
    return chunk_name

def make_namedict(audio, n, row):
    '''make name dict for naming the chunk'''
    basename = os.path.splitext(os.path.basename(audio))[0]
    coln = 0
    name_dict = {"[n]":n, 
                 "[basename]": basename}
    for value in row:
        coln = coln + 1
        name_dict["[col"+str(coln)+"]"] = value

    return name_dict

def possible_variables():
    '''Define possible naming variables, in regex form'''

    variables = [r'\[basename\]',   # file basename
                 r'\[col[0-9]+\]',  # column number, from tab delimted txt
                 r'\[n\]']          # chunk number
    valid_pattern = string.join(variables, "|")
    return valid_pattern

def read_chunks(chunks, header):
    txtfile = open(chunks,'rb')
    chunkreader = csv.reader(txtfile, delimiter = "\t")
    if header:
        head = chunkreader.next()
    return chunkreader

def read_naming(naming):
    '''Read naming.config, and check that it is valid'''

    variable_pattern = re.compile(r'\[.*?\]')
    variables = re.findall(variable_pattern, naming)
    valid_pattern = possible_variables()
    for var in variables:
        if not re.match(valid_pattern, var):
            raise NamingException("%s not a valid naming variable, "
                                  "see help chunkup.py -h"%var)
    return (variables, naming)


def setup_parser():
    '''set up argument parser'''
    parser = argparse.ArgumentParser(description = ("Takes audio file and "
                                     "tab delimited file as input. "
                                     "Chunk onset and offset must be in "
                                     "ss.ms format"),
                                     fromfile_prefix_chars="+")
    parser.add_argument("audio",
                        help = "The audio file to chunkup. "
                        "It can be any audio file sox can process.")
    parser.add_argument("chunks",
                        help = "A tab delimited file defining chunks")
    parser.add_argument("outdir",
                        help = "output directory for chunks")
    parser.add_argument("--naming", "-n",
                        default = "[n]-[basename]-[col1]-[col3].wav",
                        help = ("string defining the filename formatting "
                                "for each chunk. Possible values are:\n "
                                "[basename]: basename of original audio,\n"
                                "[n]: chunk number,\n"
                                "[col0-9]: values from the specified "
                                "columns in the chunk file."))
    parser.add_argument("--start", "-s", type = int,
                        default = 3,
                        help = "Column number for chunk start")
    parser.add_argument("--end", "-e", type = int,
                        default = 4,
                        help = "Column number for chunk end")
    parser.add_argument("--header", action = "store_true",
                        help = "Include flag if chunk file has a header")
    return parser

def chunkup(audio, chunks, outdir, naming, start, end, header=False):
    '''Main chunkup procedure'''

    check_outdir(outdir)
    
    variables, config_string = read_naming(naming)

    # chunkreader is a csv.reader iterable
    chunkreader = read_chunks(chunks, header)

    n = 0
    for row in chunkreader:
        n = n+1

        name_dict = make_namedict(audio, n, row)
        chunk_name = make_chunkname(variables, config_string, name_dict)
        outfile = os.path.join(outdir, chunk_name)

        start_time = float(row[start-1])
        end_time   = float(row[end-1])
        dur = end_time-start_time

        chunk_audio(audio, outfile, str(start_time), str(dur))

if __name__ == '__main__':
    parser = setup_parser()
    opts = parser.parse_args()

    chunkup(audio = opts.audio, 
            chunks = opts.chunks, 
            outdir = opts.outdir,
            naming = opts.naming, 
            start = opts.start,
            end = opts.end,
            header = opts.header)

