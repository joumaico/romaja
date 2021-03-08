import itertools

from .const import BASE, SPAN
from .utils import decompose, scan


def transliterate(text: str) -> str:
    """
    Transliteration of Korean alphabet (Hangul) in the Latin script.

    Parameters
    ----------
    text : str
        UTF-8 characters

    Returns
    ----------
    transliterate : str
    """

    MIX = BASE['MIX']

    def process(word: str) -> str:
        result = []
        chunks = list(itertools.chain(*[decompose(c) for c in f" {word} "]))
        for i in range(1, len(chunks[:-1])):
            if (i + 1) % 3 == 0:  # [tail, head, mean]
                rows = [chunks[i], chunks[i + 1], chunks[i + 2]]
                form = [''] * 3
                if (mean := scan(rows[2])):
                    form[2] = mean
                try:
                    form[0] = SPAN[rows[0]][rows[1]]
                    form[1] = ''
                except KeyError:
                    if (mix := MIX.get(rows[0])):
                        if rows[1] == 'ㅇ':
                            form[0] = SPAN[mix[0]][mix[1]]
                        else:
                            form[0] = scan(mix[0])[1]
                    if (tail := scan(rows[0])):
                        form[0] = tail[0 if rows[1] == 'ㅇ' else 1]
                    if (lead := scan(rows[1])):
                        form[1] = lead[0]
                if not form[1] and not scan(rows[1]):
                    form[1] = rows[1]
                result.append(form)
        return ''.join(itertools.chain(*result))

    return ' '.join(map(process, text.split(' ')))
