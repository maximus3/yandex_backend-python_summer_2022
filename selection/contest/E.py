def main(line=None, f=None):
    idx_op = -1
    idx_cl = -1
    was_neg = False
    was_sec_type = False

    cnt = 0
    s_cnt = 0
    i = 1
    while True:
        if f:
            c = f.read(1)
            if c == '\n':
                break
        else:
            if i == len(line) + 1:
                break
            c = line[i - 1]
        if c == '(':
            s_cnt += 1
            if not was_neg and cnt == 0:
                idx_op = i
            cnt += 1
        elif c == ')':
            s_cnt += 1
            cnt -= 1
            if not was_neg and not was_sec_type:
                idx_cl = i
            was_sec_type = True
            if cnt < 0:
                if was_neg:
                    return -1
                was_neg = True
                if idx_cl == -1:
                    idx_cl = i
                cnt = 0
        i += 1
    if s_cnt % 2 == 0:
        return -1
    if cnt == 0 and was_neg:
        return idx_cl
    if cnt == 1 and not was_neg:
        return idx_op
    return -1


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        res = main(f=f)
    print(res)
