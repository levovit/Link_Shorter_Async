from random import randint


def convert_base(num, to_base=10, from_base=10) -> str:
    # first convert to decimal number
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    # now convert decimal to 'to_base' base
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]


def make_link(host: str) -> str:
    random_number = randint(1, 1_000_000)  # 1 million unique links
    return host + "/" + convert_base(random_number, 35)
