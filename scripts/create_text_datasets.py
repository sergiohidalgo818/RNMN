"""Script that creates 3 data sets files for text training 
     IT MUST BE EXECUTED from THE UPPER DIRECTORY"""

import string
from itertools import permutations
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


MAX_CHARS = 8

def lexic_data(file_name):
    """Creates a data set with 4 columns (one for each ASCII binary lexic number)
      and 10 classes (one for each number) 

    Args:
    file_name (str): path to the file

    Returns:
        None
        """

    num_of_bits = 8  # each character is 8 bits long in ASCII

    nums = ['uno', 'dos', 'tres', 'cuatro',
            'cinco', 'seis', 'siete', 'ocho', 'nueve']

    classes = ['1000000000', '0100000000', '0010000000',
               '0001000000', '0000100000', '0000010000',
               '0000001000', '0000000100', '0000000010',
               '0000000001']

    nums_and_classes = zip(nums, classes)

    abecedary = list(string.printable)

    # create dictionary
    entries = ['x'+str(i) for i in range(0, MAX_CHARS*num_of_bits, 1)] 
    outputs = ['y'+str(i) for i in range(0, 10, 1)]
    data_dict = {key: list() for key in (entries + outputs)}

    print("Creating lexic dataset")

    for inum, iclass in nums_and_classes:
        list_of_pattern = list
        size = len(inum)

        max_extra_chars = MAX_CHARS - size
        permutations_abecedary = permutations(abecedary, r=max_extra_chars)

        number_bin = ""

        number_bin = ''.join('{0:08b}'.format(ord(x), 'b') for x in inum)

        for perm in permutations_abecedary:
            bin_num_perm = ''.join('{0:08b}'.format(ord(x), 'b') for x in perm)

            number = bin_num_perm
            number += number_bin 

            # ASCII characters at the begining of the number
            for inumber, key in zip(number, entries):
                data_dict[key].append(inumber)
            for inumber, key in zip(iclass, outputs):
                data_dict[key].append(inumber)

            number = number_bin
            number += bin_num_perm

            # ASCII characters at the end of the number
            for inumber, key in zip(number, entries):
                data_dict[key].append(inumber)
            for inumber, key in zip(iclass, outputs):
                data_dict[key].append(inumber)


            for num_slash in range(1, max_extra_chars-1, 1):

                mid_slash = int(len(bin_num_perm)/(max_extra_chars/num_slash))
                number = bin_num_perm[:mid_slash]
                number += number_bin
                number += bin_num_perm[mid_slash:]
                
                for inumber, key in zip(number, entries):
                    data_dict[key].append(inumber)
                for inumber, key in zip(iclass, outputs):
                    data_dict[key].append(inumber)


    print("Writing lexic dataset...")
    data_frame = pd.DataFrame(data_dict)
    table = pa.Table.from_pandas(data_frame)
    pq.write_table(table, file_name)
    print("Lexic dataset done")

def hex_data(file_name):
    """Creates a data set with 4 columns (one for each ASCII binary number)
      and 10 classes (one for each number) 

    Args:
    file_name (str): path to the file

    Returns:
        None
        """

    nums = [''.join('{0:08b}'.format(ord(str(num)), 'b')) for num in range(0,10,1)]

    classes = ['1000000000', '0100000000', '0010000000',
               '0001000000', '0000100000', '0000010000',
               '0000001000', '0000000100', '0000000010',
               '0000000001']

    nums_and_classes = zip(nums, classes)


    # create dictionary
    entries = ['x'+str(i) for i in range(0,8, 1)] 
    outputs = ['y'+str(i) for i in range(0, 10, 1)]
    data_dict = {key: list() for key in (entries + outputs)}

    print("creating numeric hexadecimal dataset")

    for inum, iclass in nums_and_classes:

        for inumber, key in zip(inum, entries):
                data_dict[key].append(inumber)
        for inumber, key in zip(iclass, outputs):
                data_dict[key].append(inumber)

    print("Writing hexadecimal dataset...")
    data_frame = pd.DataFrame(data_dict)
    table = pa.Table.from_pandas(data_frame)
    pq.write_table(table, file_name)
    print("Done")


def binary_data(file_name):
    """Creates a data set with 4 columns (one for each binary number)
      and 10 classes (one for each number) 

    Args:
    file_name (str): path to the output file

    Returns:
        None
        """

    nums = ['0000', '0001', '0010', '0011', '0100',
            '0101', '0110', '0111', '1000', '1001']

    classes = ['1000000000', '0100000000', '0010000000',
               '0001000000', '0000100000', '0000010000',
               '0000001000', '0000000100', '0000000010',
               '0000000001']

    nums_and_classes = zip(nums, classes)


    # create dictionary
    entries = ['x'+str(i) for i in range(0,4, 1)] 
    outputs = ['y'+str(i) for i in range(0, 10, 1)]
    data_dict = {key: list() for key in (entries + outputs)}

    print("creating numeric binary dataset")

    for inum, iclass in nums_and_classes:

        for inumber, key in zip(inum, entries):
                data_dict[key].append(inumber)
        for inumber, key in zip(iclass, outputs):
                data_dict[key].append(inumber)

    print("Writing binary dataset...")
    data_frame = pd.DataFrame(data_dict)
    table = pa.Table.from_pandas(data_frame)
    pq.write_table(table, file_name)
    print("Done")


if __name__ == '__main__':

    directory = 'data/text_data/'
    
    hex_data(directory+"hex_data.parquet")

    binary_data(directory+"binary_data.parquet")
    
    lexic_data(directory+"text_data.parquet")