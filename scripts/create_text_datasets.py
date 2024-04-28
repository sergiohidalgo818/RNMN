"""Script that creates 3 data sets files for text training and 3
     datasets for testing IT MUST BE EXECUTED from THE UPPER DIRECTORY"""

import string
from itertools import permutations
import random
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
import os

MAX_CHARS = 8
MAX_CHARS_WORD = 6

def _bin_array(x:str)-> np.ndarray:
    """Transforms a string of binary string to a numpy array

    Args:
    x (str): binary string

    Returns:
        The numpy array
        """
    list = [int(char) for char in x]
    return np.array(list)

def _np_assign(x)->np.ndarray:
    """Assigns the 1 value to the output

        Args:
        x (int): index of the value

        Returns:
            The numpy array
            """
    np_array=np.zeros((10,),dtype=int)
    np_array[x]=1
    return np_array


classes = [_np_assign(x) for x in range(0, 10, 1)]


def noise_lexic_data(file_name, ascii_perm_size):
    """Creates a dataset with 4 columns (one for each ASCII binary lexic number)
      and 10 classes (one for each number)

    Args:
    file_name (str): path to the file
    ascii_perm_size (int): size of the random abecedary
      of ASCII characters

    Returns:
        None
        """

    num_of_bits = 8  # each character is 8 bits long in ASCII

    nums = ['cero', 'uno', 'dos', 'tres', 'cuatro',
            'cinco', 'seis', 'siete', 'ocho', 'nueve']

    nums_and_classes = zip(nums, classes)

    abecedary = list(string.printable)

    # create dictionary
    entries = ['x'+str(i) for i in range(0, MAX_CHARS*num_of_bits, 1)]
    outputs = ['y'+str(i) for i in range(0, 10, 1)]
    data_dict = {key: list() for key in (entries + outputs)}

    print("\nCreating lexic dataset")

    for inum, iclass in nums_and_classes:

        size = len(inum)

        max_extra_chars = MAX_CHARS - size

        random.shuffle(abecedary)
        permutations_abecedary = permutations(
            abecedary[:ascii_perm_size], r=max_extra_chars)

        number_bin = ""

        number_bin = ''.join('{0:08b}'.format(ord(x), 'b') for x in inum)

        for perm in permutations_abecedary:

            perm_contains_num = False
            text_perm = ''.join('{}'.format(x) for x in perm)

            # check if there is a string number in the permutation
            for jnum in nums:
                if text_perm in jnum:
                    perm_contains_num = True

            # if there is, ignore iteration
            if (perm_contains_num == False):
                bin_num_perm = ''.join(
                    '{0:08b}'.format(ord(x), 'b') for x in perm)

                number = bin_num_perm
                number += number_bin

                number = _bin_array(number)
                # ASCII characters at the begining of the number
                for inumber, key in zip(number, entries):
                    data_dict[key].append(inumber)
                for inumber, key in zip(iclass, outputs):
                    data_dict[key].append(inumber)

                number = number_bin
                number += bin_num_perm
                number = _bin_array(number)

                # ASCII characters at the end of the number
                for inumber, key in zip(number, entries):
                    data_dict[key].append(inumber)
                for inumber, key in zip(iclass, outputs):
                    data_dict[key].append(inumber)

                for num_slash in range(1, max_extra_chars-1, 1):

                    mid_slash = int(len(bin_num_perm) /
                                    (max_extra_chars/num_slash))
                    
                    number = bin_num_perm[:mid_slash]
                    number += number_bin
                    number += bin_num_perm[mid_slash:]
                    number = _bin_array(number)

                    for inumber, key in zip(number, entries):
                        data_dict[key].append(inumber)
                    for inumber, key in zip(iclass, outputs):
                        data_dict[key].append(inumber)

    print("Writing lexic dataset...")
    data_frame = pd.DataFrame(data_dict)
    table = pa.Table.from_pandas(data_frame)
    pq.write_table(table, file_name)
    print("Lexic dataset done")


def lexic_data(file_name):
    """Creates a dataset with 4 columns (one for each ASCII binary lexic number)
      and 10 classes (one for each number)

    Args:
    file_name (str): path to the file

    Returns:
        None
        """

    num_of_bits = 8  # each character is 8 bits long in ASCII

    nums = ['cero', 'uno', 'dos', 'tres', 'cuatro',
            'cinco ', 'seis', 'siete', 'ocho', 'nueve']

    nums_and_classes = zip(nums, classes)

    # create dictionary
    entries = ['x'+str(i) for i in range(0, num_of_bits*MAX_CHARS, 1)]
    outputs = ['y'+str(i) for i in range(0, 10, 1)]
    data_dict = {key: list() for key in (entries + outputs)}

    print("\nCreating lexic dataset")

    for inum, iclass in nums_and_classes:

        number_bin = ""

        number_bin = ''.join('{0:08b}'.format(ord(x), 'b') for x in inum)
        
        # add extra zeros to the string
        aux_zeros = ''.join('{0:01b}'.format(0, 'b') for x in range(
            num_of_bits*MAX_CHARS - len(number_bin)))

        # with zeros before and zeros after (spaces)
        number_bin_zeros = number_bin + aux_zeros
        zeros_number_bin = aux_zeros + number_bin

        # keep it as integers so its keeped as integers on parquet
        number_bin_zeros = _bin_array(number_bin_zeros) 
        zeros_number_bin = _bin_array(zeros_number_bin) 

        for inumber_zeros,izeros_number, key in zip(number_bin_zeros,zeros_number_bin, entries):
            data_dict[key].append(inumber_zeros)
            data_dict[key].append(izeros_number)
        for inumber, key in zip(iclass, outputs):
            data_dict[key].append(inumber)
            data_dict[key].append(inumber)

    print("Writing lexic dataset...")
    data_frame = pd.DataFrame(data_dict)
    table = pa.Table.from_pandas(data_frame)
    pq.write_table(table, file_name)
    print("Lexic dataset done")


def hex_data(file_name):
    """Creates a dataset with 8 columns (one for each ASCII binary number)
      and 10 classes (one for each number) UNUSED

    Args:
    file_name (str): path to the file

    Returns:
        None
        """
    

    nums = [''.join('{0:08b}'.format(ord(str(num)), 'b'))
            for num in range(0, 10, 1)]
    
    # keep it as integers so its keeped as integers on parquet
    nums = [_bin_array(num) for num in nums]

    nums_and_classes = zip(nums, classes)

    # create dictionary
    entries = ['x'+str(i) for i in range(0, 8, 1)]
    outputs = ['y'+str(i) for i in range(0, 10, 1)]
    data_dict = {key: list() for key in (entries + outputs)}

    print("\nCreating numeric hexadecimal dataset")

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
    """Creates a dataset with 4 columns (one for each binary number)
      and 10 classes (one for each number) UNUSED

    Args:
    file_name (str): path to the output file

    Returns:
        None
        """

    nums = ['0000', '0001', '0010', '0011', '0100',
            '0101', '0110', '0111', '1000', '1001']
    
    # keep it as integers so its keeped as integers on parquet
    nums = [_bin_array(num) for num in nums]

    nums_and_classes = zip(nums, classes)

    # create dictionary
    entries = ['x'+str(i) for i in range(0, 4, 1)]
    outputs = ['y'+str(i) for i in range(0, 10, 1)]
    data_dict = {key: list() for key in (entries + outputs)}

    print("\nCreating numeric binary dataset")

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

    train_directory = 'data/text_data/train/'
    if not os.path.exists(train_directory):
        print("Creating data text train directory")
        os.makedirs(train_directory)

    test_directory = 'data/text_data/test/'
    if not os.path.exists(test_directory):
        print("Creating data text test directory")
        os.makedirs(test_directory)


    lexic_data(train_directory+"lexic_data.parquet")
    noise_lexic_data(train_directory+"noise_lexic_data.parquet", 6)

    noise_lexic_data(test_directory+"noise_lexic_data.parquet", 4)
