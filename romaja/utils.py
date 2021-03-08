from typing import Union, List

from .const import BASE, TAIL

LEAD = [*BASE['CONSONANT']]
MEAN = [*BASE['VOWEL']]

LEN_MEAN = len(MEAN)
LEN_TAIL = len(TAIL)

LETTERS = {**BASE['CONSONANT'], **BASE['VOWEL']}


def decompose(c: str) -> List[str]:
    # hangul chars in-between 0xAC00 -> 0xD7A3 or '가' -> '힣'
    if 0xAC00 <= (position := ord(c)) <= 0xD7A3:
        code = position - 0xAC00
        tail = int(code % LEN_TAIL)
        code /= LEN_TAIL
        mean = int(code % LEN_MEAN)
        code /= LEN_MEAN
        lead = int(code)
        return [LEAD[0 if lead < 0 else lead], MEAN[mean], TAIL[tail]]
    return ['' if c == ' ' else c, '', '']


def scan(letter: str) -> Union[List[str], str, None]:
    # scan values of hangul chars: consonant and vowel
    if (x := LETTERS.get(letter)):
        return x
    return
