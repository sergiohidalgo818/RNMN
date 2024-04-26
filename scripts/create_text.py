"""Script that creates a file named text_data.txt on data/text_data
     directory IT MUST BE EXECUTED ON THE UPPER DIRECTORY"""

import string
from itertools import permutations
from math import ceil

MAX_CHARS = 8

if __name__ == '__main__':
    file = open("data/text_data/text_data.txt", 'w')

    num_of_bits = 8  # each character is 8 bits long in ASCII

    file.write(str(MAX_CHARS*num_of_bits)+" 10\n")

    nums = ['u n o', 'd o s', 't r e s', 'c u a t r o',
            'c i n c o', 's e i s', 's i e t e', 'o c h o', 'n u e v e']
    classes = ['1 0 0 0 0 0 0 0 0 0', '0 1 0 0 0 0 0 0 0 0', '0 0 1 0 0 0 0 0 0 0',
               '0 0 0 1 0 0 0 0 0 0', '0 0 0 0 1 0 0 0 0 0', '0 0 0 0 0 1 0 0 0 0',
               '0 0 0 0 0 0 1 0 0 0', '0 0 0 0 0 0 0 1 0 0', '0 0 0 0 0 0 0 0 1 0',
               '0 0 0 0 0 0 0 0 0 1']

    nums_and_classes = zip(nums, classes)

    abecedary = list(string.printable)

    base = 16  # hexadecimal

    for inum, iclass in nums_and_classes:
        list_of_pattern = list
        size = len(inum)

        letters = int(size/2) + 1

        max_extra_chars = MAX_CHARS - letters
        permutations_abecedary = permutations(abecedary, r=max_extra_chars)
    
        aux_num = inum.replace(" ", "")
        number_bin = ""

        number_bin= ''.join('{0:08b}'.format(ord(x), 'b') for x in aux_num)
        number_bin = number_bin.replace("", " ")[1: -1]

        for perm in permutations_abecedary:
            bin_num_perm = ''.join('{0:08b}'.format(ord(x), 'b') for x in perm)
            bin_num_perm = bin_num_perm.replace("", " ")[1: -1]

            number = bin_num_perm + ' '
            number += number_bin + ' '
            number += iclass

            # ASCII characters at the begining of the number
            file.write(number + "\n")

            number = number_bin + ' '
            number += bin_num_perm + ' '
            number += iclass

            # ASCII characters at the end of the number
            file.write(number + "\n")


            for num_slash in range(1,max_extra_chars-1,1):

                mid_slash = int(len(bin_num_perm)/(max_extra_chars/num_slash))
                number = bin_num_perm[:mid_slash] + ' '
                number += number_bin + ' '
                number += bin_num_perm[mid_slash:] + ' '
                number += iclass
                    
                file.write(number + "\n")
