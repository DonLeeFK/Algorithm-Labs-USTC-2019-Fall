def backtrace(ti,n,k):
    def _util(i,arrange):
        nonlocal total_time,rst,machine_time
        if i==n:
            total_time=getTime()
            rst=arrange.copy()
        else:
             for j in range(k):
                machine_time[j]+=ti[i]
                if total_time is None or getTime()<total_time:
                    arrange[i]=j
                    _util(i+1,arrange)
                machine_time[j]-=ti[i]
    def getTime():
        return max(machine_time)
    total_time=None
    rst=None
    machine_time=[0 for i in range(k)]
    _util(0,[-1]*n)
    return total_time, rst


import random
from time import time

def testbr_auto():
    global start
    k=random.randint(1,8)
    n=random.randint(k,16)
    ti=[random.randint(1,100) for i in range(n)]
    print("k=",k)
    print("n=",n)
    print('time for i_th task:',end='')
    print(ti)
    print('result: ',end='')
    start=time()
    print(backtrace(ti,n,k))


def testbr_manual():
    global start
    k=int(input("k="))
    ti=[int(x) for x in input().split()]
    print("k=",k)
    n=len(ti)
    print("n=",n)
    print('time for i_th task:')
    print(ti)
    print('result: ',end='')
    start=time()
    print(backtrace(ti,n,k))

print("1.auto\n2.manual")
flag=int(input())
if flag is 1:
    testbr_auto()
elif flag is 2:
    testbr_manual()
print('time  : {:.6f} s'.format(time() - start))