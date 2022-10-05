def fill(data, queue, x, y, cur):
    if x >= len(data) or y >= len(data[x]):
        return
    if data[x][y] != '.' and cur != 'S':
        return
    data[x][y] = cur
    if cur != 'U':
        queue.append((x + 1, y, 'D'))
    if cur != 'D':
        queue.append((x - 1, y, 'U'))
    if cur != 'L':
        queue.append((x, y + 1, 'R'))
    if cur != 'R':
        queue.append((x, y - 1, 'L'))


def main(n, m, data):
    queue = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 'S':
                queue.append((i, j, 'S'))
                break
        else:
            continue
        break
    while len(queue):
        args = queue.pop()
        fill(data, queue, *args)
    return list(map(''.join, data))


if __name__ == '__main__':
    n, m = input().split()
    n, m = int(n), int(m)
    data = [list(input()) for _ in range(n)]
    res = main(n, m, data)
    print(*res, sep='\n')
