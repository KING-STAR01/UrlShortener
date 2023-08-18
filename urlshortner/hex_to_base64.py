#convert string to binary divide the string into sextets again convert it to base 64

import textwrap
from typing import List

CHARS_IN_BASE64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def convert_to_binary(char: str) -> str:
    """
    converts a char to 8bit binary
    @param: char
    @return: binary string
    """
    num = ord(char)
    binary = ""
    while num > 1:
        rem = num % 2
        num = num // 2
        binary = str(rem) + binary
    if num:
        binary = str(num) + binary
    binary = binary.rjust(8, '0')
    return binary

def str_to_binary(string: str) -> str:
    binary = ""
    for char in string:
        binary += convert_to_binary(char)
    return binary

def get_sextets(binary: str) -> List[str]:
    group_size = 6
    sextets = textwrap.wrap(binary, group_size)
    return sextets

def bin_to_dec(binary: str) -> int:
    num = 0
    for i in binary[:-1]:
        num = (num + int(i)) * 2
    num += int(binary[-1])
    return num

def convert_to_base64(sextets: List[str]) -> str:
    base64_str = ""
    for sextet in sextets:
        if len(sextet) < 6:
            sextet = sextet.ljust(6, '0')
        print(sextet)
        base64_ref = bin_to_dec(sextet)
        base64_str += CHARS_IN_BASE64[base64_ref]
    return base64_str

def dec_to_base64(num: int) -> str:
    ret = ""
    while num:
        rem = num % 64
        num = num // 64
        s = CHARS_IN_BASE64[rem]
        ret = s + ret

    return ret


if __name__ == "__main__":
    binary = str_to_binary("deadbeef")
    print(binary)
    sextets = get_sextets(binary)
    print(sextets)
    print(convert_to_base64(sextets))
    #num = bin_to_dec(binary)
    #print(dec_to_base64(num))
    binary = str_to_binary("ABC")
    print(binary)
    sextets = get_sextets(binary)
    print(sextets)
    print(convert_to_base64(sextets))

