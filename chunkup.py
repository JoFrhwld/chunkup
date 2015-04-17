from pysox import CSoxApp
import argparse
import re
import string


class NamingException(Exception):
    '''An exception for chunk naming problems'''
    pass    

def possible_variables():
    '''Define possible naming variables, in regex form'''

    variables = [r'\[basename\]',   # file basename
                 r'\[col[0-9]+\]',  # column number, from tab delimted txt
                 r'\[n\]']          # chunk number
    valid_pattern = string.join(variables, "|")
    return valid_pattern


def read_naming(namingConfig):
    '''Read naming.config, and check that it is valid'''
    config_fi = open(namingConfig)
    config_string = config_fi.readlines()
    config_fi.close()

    if len(config_string) > 1:
        raise NamingException("Naming config more than 1 line.")

    variable_pattern = re.compile(r'\[.*?\]')
    variables = re.findall(variable_pattern, config_string[0])
    valid_pattern = possible_variables()
    for var in variables:
        if not re.match(valid_pattern, var):
            raise NamingException("%s not a valid naming variable, "
                                  "see help chunkup.py -h"%var)
    return (variables, config_string)


def setup_parser():
    '''set up argument parser'''
    parser = argparse.ArgumentParser(description = ("Takes .wav file and "
                                     "tab delimited file as input. "
                                     "Chunk onset and offset must be in "
                                     "ss.ms format"))
    parser.add_argument("wav",
                        help = "The wav file to chunkup")
    parser.add_argument("chunks",
                        help = "A tab delimited file defining chunks")
    parser.add_argument("--naming", "-n",
                        default = "naming.config",
                        help = ("file defining the filename formatting "
                                "for each chunk. Possible values are:\n "
                                "[basename]: basename of original wav,\n"
                                "[n]: chunk number,\n"
                                "[col0-9]: values from the specified "
                                "columns in the chunk file."))
    return parser

if __name__ == '__main__':
    parser = setup_parser()
    opts = parser.parse_args()

    variables, config_string = read_naming("naming.config")
    print variables