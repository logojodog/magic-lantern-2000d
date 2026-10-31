import re

def word_wrap(text, width, extent_func):
    lines = []
    pattern = re.compile(r'(\s+)')
    lookup = dict((c, extent_func(c)[0]) for c in set(text))
    for line in text.splitlines():
        tokens = pattern.split(line)
        tokens.append('')
        widths = [sum(lookup[c] for c in token) for token in tokens]
        start, total = 0, 0
        for index in range(0, len(tokens), 2):
            if total + widths[index] > width:
                end = index + 2 if index == start else index
                lines.append(''.join(tokens[start:end]))
                start, total = end, 0
                if end == index + 2:
                    continue
            total += widths[index] + widths[index + 1]
        if start < len(tokens):
            lines.append(''.join(tokens[start:]))
    lines = [line.strip() for line in lines]
    return lines or ['']
