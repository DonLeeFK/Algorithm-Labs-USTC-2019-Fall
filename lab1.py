from functools import total_ordering
from random import randint
from random import uniform
from time import time

def floatEql(f1, f2, epsilon=1e-15):
    return abs(f1 - f2) < epsilon
def findif(points, f, reverse=False):
    n = len(points)
    rg = range(n - 1, -1, -1) if reverse else range(n)
    for i in rg:
        if not f(points[i]):
            return points[i + 1:] if reverse else points[:i]
    return points.copy()

class point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    #def __length__(self):
        #return self.norm(2)
    def __lt__(self,p):
        return self.x < p.x or (self.x == p.x and self.y < p.y)
    def __eq__(self, p):
        return self.x == p.x and self.y == p.y
    def distance(self, p):
        return ((self.x - p.x)**2 + (self.y - p.y)**2)**0.5
    def __repr__(self):
        return 'point({},{})'.format(self.x, self.y)


def minDistance(pts):
    n=len(pts)
    if n == 2: return pts[0].distance(pts[1]),pts[0],pts[1]
    if n == 3:
        minD = pts[0].distance(pts[1])
        p, q = pts[0], pts[1]
        if minD > pts[1].distance(pts[2]):
            minD = pts[1].distance(pts[2])
            p, q = pts[1], pts[2]
        if minD > pts[0].distance(pts[2]):
            minD = pts[0].distance(pts[2])
            p, q = pts[0], pts[2]
        return minD,p,q
    n2 = n // 2
    mid = (pts[n2].x + pts[n2 - 1].x) / 2
    s1 = pts[:n2]
    s2 = pts[n2:]
    minD, p, q = minDistance(s1)
    d2, p2, q2 = minDistance(s2)
    if minD > d2:
        minD, p, q = d2, p2, q2
    
    linePoints = linePoints = findif(s1, lambda pt: floatEql(pt.x, mid), reverse=True)
    linePoints += findif(s2, lambda pt: floatEql(pt.x, mid))
    n = len(linePoints)
    if n > 1:
        for i in range(1, n):
            dis = linePoints[i].y - linePoints[i - 1].y
            if dis < minD:
                minD = dis
                p, q = linePoints[i - 1], linePoints[i]
    leftPoints = findif(s1, lambda pt: pt.x >= mid - minD, reverse=True)
    rightPoints = findif(s2, lambda pt: pt.x <= mid + minD)
    for lp in leftPoints:
        y1, y2 = lp.y - minD, lp.y + minD
        for rp in rightPoints:
            if y1 < rp.y < y2:
                dis = lp.distance(rp)
                if dis < minD:
                        minD = dis
                        p, q = lp, rp
    #minD=p.distance(q)
    minD=abs(minD)
    return minD, p, q

def test_auto():
    global start
    n=randint(1,10000)
    #n=3
    x=[uniform(1,100) for i in range(n)]
    y=[uniform(1,100) for i in range(n)]
    #x=[randint(1,10) for i in range(n)]
    #y=[randint(1,10) for i in range(n)]
    pts=[]
    for i in range(n):
        pts.append(point(x[i],y[i]))
    print(pts,end='\n')
    print('\ntested {} points'.format(n))
    print("\nresult :",end='')
    start=time()
    print(minDistance(pts))

def getInput():
    str=input()
    #print("str:",str)
    pair=str.split(' ')
    #print("pair:",pair)
    arg=[i.split(',') for i in pair]
    #print("arg:",arg)
    pair_num=len(pair)
    #print("n=",n)
    pts = []
    for i in range(pair_num):
        pts.append(point(float(arg[i][0]),float(arg[i][1])))
    
    print(pts)
    return pts

def test_manual():
    global start
    print("input coordinates")
    pts=getInput()
    print("\nresult: ",end='')
    start=time()
    print(minDistance(pts))

print("1.auto\n2.manual")
flag=int(input())
if flag is 1:
    test_auto()
elif flag is 2:
    test_manual()
print('time   : {:.6f} s'.format(time() - start))
