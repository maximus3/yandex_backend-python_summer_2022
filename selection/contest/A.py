from collections import Counter
from enum import Enum


class CharType(str, Enum):
    CORRECT = 'correct'
    PRESENT = 'present'
    ABSENT = 'absent'


def main(s, q):
    n = len(s)
    data = [CharType.ABSENT] * n
    counter = Counter(s)
    for i in range(n):
        if s[i] == q[i]:
            data[i] = CharType.CORRECT
            counter[s[i]] -= 1
    for i in range(n):
        if data[i] == CharType.CORRECT:
            continue
        if counter[q[i]] > 0:
            counter[q[i]] -= 1
            data[i] = CharType.PRESENT
    return [val.value for val in data]


if __name__ == '__main__':
    s = input()
    q = input()
    res = main(s, q)
    print(*res, sep='\n')
