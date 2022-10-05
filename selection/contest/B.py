from queue import PriorityQueue


def main(n, sm_data, k, cqrp_data):
    vac_data = {vac: (int(cnt), PriorityQueue()) for vac, cnt in sm_data}
    for emp_data in cqrp_data:
        name, vac, cnt, pen = emp_data.split(',')
        vac_data[vac][1].put((int(cnt), -int(pen), name))
        if vac_data[vac][1].qsize() > vac_data[vac][0]:
            vac_data[vac][1].get_nowait()
    emps = []
    for vac in vac_data:
        while vac_data[vac][1].qsize() > 0:
            emps.append(vac_data[vac][1].get_nowait()[2])
    return sorted(emps)


if __name__ == '__main__':
    n = int(input())
    sm_data = [input().split(',') for _ in range(n)]
    k = int(input())
    cqrp_data = [input() for _ in range(k)]
    res = main(n, sm_data, k, cqrp_data)
    print(*res, sep='\n')
