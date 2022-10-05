def is_right(s):
    cnt = 0
    for c in s:
        if c == '(':
            cnt += 1
        elif c == ')':
            cnt -= 1
            if cnt == -1:
                return False
    return cnt == 0


def main(s):
    n = len(s)
    for i in range(n):
        if s[i] != '(' and s[i] != ')':
            continue
        s_new = s[:i] + s[i + 1:]
        if is_right(s_new):
            return i + 1
    return -1


if __name__ == '__main__':
    print(main(input()))
