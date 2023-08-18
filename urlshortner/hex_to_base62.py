CHARS_IN_62 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

def convert_to_int(char: str) -> int:
    if '0' <= char <= '9':
        return int(char)
    elif 'a' <= char <= 'f':
        return 10 + ord(char) - ord('a')
    else:
        return -1

def hex_to_dec(hex: str) -> int:
    num = 0
    for char in hex[:-1]:
        int_val = convert_to_int(char)
        num = (num + int_val) * 16
    num += convert_to_int(hex[-1])
    return num

def dec_to_base62(num: int) -> str:
    encoded_str = ""
    while num:
        rem = num % 62
        num = num // 62
        encoded_str = CHARS_IN_62[rem] + encoded_str

    return encoded_str

def main(hex_string: str) -> str:
    num = hex_to_dec(hex_string)
    base_62_str = dec_to_base62(num)
    return base_62_str


if __name__ == "__main__":
    print(main("deadbeef"))




