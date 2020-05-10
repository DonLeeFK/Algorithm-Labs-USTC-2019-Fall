import networkx as nx
import multiprocessing as mp
from collections import deque


class UDG:
    def __init__(self):
        self.nodes = set()
        self.G = nx.Graph()
    
    def addEdge(self, inKey, outKey):
        self.nodes.add(inKey)
        self.nodes.add(outKey)
        self.G.add_edge(inKey, outKey)
    
    def bfs(self, src, dst):
        self.dq = deque()
        self.dq.append(src)
        self.visited = set()
        self.visited.add(src)
        path = []
        while self.dq:
            cur = self.dq.popleft()
            path.append(cur)
            if cur == dst:
                break
            for nd in self.G.adj[cur].keys():
                if nd not in self.visited:
                    if nd in self.nodes:
                        self.dq.append(nd)
                    self.visited.add(nd)
        print('->'.join(path))
        print(len(path))

    
    def bi_bfs(self, src, dst):
        self.sdq = deque()
        self.ddq = deque()
        self.svisited = set()
        self.dvisited = set()
        self.visited = set()
        self.visited.add(src)
        self.visited.add(dst)
        self.sdq.append(src)
        self.svisited.add(src)
        self.ddq.append(dst)
        self.dvisited.add(dst)
        spath = []
        dpath = []
        path = []

        i = 1
        while self.sdq and self.ddq:
            flag = 0
            if len(self.svisited) >= len(self.dvisited):
                #print(self.ddq)
                dcur = self.ddq.popleft()
                dpath.append(dcur)
                for nd in self.G.adj[dcur].keys():
                    if nd not in self.dvisited:
                        if nd in self.nodes:
                            self.ddq.append(nd)
                    self.visited.add(nd)
                    self.dvisited.add(nd)
    
                    if nd in self.svisited:
                        dpath.append(nd)
                        flag = 1
                        break
                
                
                '''
                print('s: ',len(self.svisited))
                print('d: ',len(self.dvisited))
                print('a',i)
                '''

            else:
                #print(self.sdq)
                scur = self.sdq.popleft()
                spath.append(scur)
                #print(self.G.adj[scur].keys())

                for nd in self.G.adj[scur].keys():
                    #print(self.G.adj[scur].keys())
                    if nd not in self.svisited:
                        if nd in self.nodes:
                            self.sdq.append(nd)
                            #print(self.sdq)
                    self.visited.add(nd)
                    self.svisited.add(nd)
                    if nd in self.dvisited:
                        spath.append(nd)
                        flag = 1
                        break

                    
                '''        
                print('s: ',len(self.svisited))
                print('d: ',len(self.dvisited))
                print('b',i)
                 '''
               
            if dpath and spath:
                if dpath[-1] == spath[-1]:
                    flag = 1
            
            if flag: break
                
            

            i += 1
         
        for j in range(len(dpath)):
            for i in range(len(spath)):
                if spath[i] == dpath[j]:
                    spath = spath[:i+1]
                    dpath = dpath[:j+1]
                    break
                   
        
        if spath[-1] == dpath[-1]:
            del dpath[len(dpath)-1]
        dpath.reverse()
        for nd in spath:
            path.append(nd)
        for nd in dpath:
            path.append(nd)
        print('->'.join(path))
        #print('->'.join(spath))
        #print('->'.join(dpath))
          

        '''   
        end = '-' * (180) + '\n'
        print('->'.join(spath))
        print(len(spath))
        print(end)
        print('->'.join(dpath))
        print(len(dpath))
        print(list(set(spath).intersection(set(dpath))))
        #print('->'.join(path))
        '''     
def vis_f(line):
    a, b = line.split(' ')
    b = b.replace('\n', '')
    return a, b

def readData(filename):
    with open(filename) as f:
        for line in f:  # this read method is the best
            yield vis_f(line)

from random import randint
if __name__ == '__main__':
    filename = 'facebook_combined.txt'
    udg = UDG()
    for a, b in readData(filename):
        udg.addEdge(a, b)


    #udg.bfs('114', '514')
    udg.bfs(str(randint(0,4039)), str(randint(0,4039)))
    #udg.bi_bfs(str(randint(0,4039)), str(randint(0,4039)))
    #udg.bi_bfs('1919', '810')



    




    

