from random import randint
from functools import total_ordering
class node:
    def __init__(self,val,lchild=None,rchild=None,isBlack=False):
        self.val = val
        self.lchild = lchild
        self.rchild = rchild
        self.isBlack = isBlack
    

    def setChild(self, nd, isLeft=True):
        if isLeft: self.lchild = nd
        else: self.rchild = nd
    
    def getChild(self, isLeft):
        if isLeft:
            return self.lchild
        else:
            return self.rchild
    

    


    
class RBTree:
    def __init__(self,unique = False):
        self.root = None
        self.unique = unique
    
    @staticmethod
    def getNodeisBlack(nd):
        return nd is None or nd.isBlack

    @staticmethod
    def setBlack(nd,isBlack):
        if nd is not None:
            if isBlack is None or isBlack:
                nd.isBlack = True
            else:
                nd.isBlack = False

    def setRoot(self, nd):
        if nd is not None: nd.parent = None
        self.root = nd

    
    
    def find(self, val):
        nd = self.root
        while nd:
            if nd.val == val:
                return nd
            else:
                nd = nd.getChild(nd.val > val)

    def copyNode(self, src, des):
        des.val = src.val

    def getParent(self,child):
        if self.root is child: return None
        nd = self.root
        while nd:
            if nd.val > child.val and nd.lchild is not None:
                if nd.lchild is child: return nd
                else: nd = nd.lchild
            elif nd.val < child.val and nd.rchild is not None:
                if nd.rchild is child: return nd
                else: nd  = nd.child

    def getSuccessor(self,nd):
        if nd:
            if nd.rchild:
                nd = nd.rchild
                while nd.lchild:
                    nd = nd.lchild
                return nd

            else: return self.getParent(nd)

    def transferParent(self, origin, new):
        if origin is self.root:
            self.root = new
        else:
            parent = self.getParent(origin)
            parent.setChild(new, parent.lchild is origin)

    def rotate(self, prt, chd):
        '''rotate prt with the center of chd'''
        if self.root is prt:
            self.setRoot(chd)
        else:
            prt.parent.setChild(chd, prt.parent.left is prt)
        isLeftChd = prt.left is chd
        prt.setChild(chd.getChild(not isLeftChd), isLeftChd)
        chd.setChild(prt, not isLeftChd)

    def insert(self, nd):
        if nd.isBlack: nd.isBlack = False

        if self.root is None:
            self.setRoot(nd)
            self.root.isBlack = True
        else:
            parent = self.root
            while parent:
                if parent == nd: return None
                isLeft = parent > nd
                chd = parent.getChild(isLeft)
                if chd is None:
                    parent.setChild(nd, isLeft)
                    break
                else:
                    parent = chd
            self.fixupInsert(parent, nd)

    def fixupInsert(self,parent,nd):
        while not self.getNodeisBlack(parent):
            grand = self.getParent(parent)
            isLeftParent = grand.lchild is parent
            uncle = grand.getChild(not isLeftParent)
            #case1 uncle is red
            if not self.getNodeisBlack(uncle):
                self.setBlack(grand,False)
                self.setBlack(grand.lchild, True)
                self.setBlack(grand.rchild, True)
                nd = grand
                parent = self.getParent(nd)
            #case2,3 uncle is black
            else:
                #case2 parent and nd not on the same side
                isLeftNode = parent.left is nd
                #case2 parent and nd not on the same side
                if isLeftNode^isLeftParent:
                    self.rotate(parent, nd)
                    nd, parent = parent, nd
                    #ROTATE
                #case3 parent and nd on the same side
                    grand.setChild(parent.getChild(not isLeftParent), isLeftParent)
                    parent.setChild(grand, not isLeftParent)
                    self.setBlack(grand,False)
                    self.setBlack(parent,True)
                    self.transferParent(grand,parent)
        self.setBlack(self.root,True)

    def delete(self, val):
        '''delete node in a binary search tree'''
        if isinstance(val, node): val = val.val
        nd = self.find(val)
        if nd is None: return
        self._delete(nd)
    
    def _delete(self, nd):
        y = None
        if nd.lchild and nd.rchild:
            y = self.getSuccessor(nd)
        else:
            y = nd
        py = y.parent
        x = y.lchild if y.lchild else y.rchild
        if py is None:
            self.setRoot(x)
        else:
            py.setChild(x, py.left is y)
        if y != nd:
            self.copyNode(y, nd)
        if self.getNodeisBlack(y): self.fixupDelete(py, x)

    def fixupDelete(self, prt, chd):
        ''' adjust colors and rotate '''
        while self.root != chd and self.getNodeisBlack(chd):
            isLeft = prt.left is chd
            brother = prt.getChild(not isLeft)
            # brother is black
            lb = self.getNodeisBlack(brother.getChild(isLeft))
            rb = self.getNodeisBlack(brother.getChild(not isLeft))
            if not self.getNodeisBlack(brother):
                # case 1: brother is red.   converted to  case 2,3,4

                self.setBlack(prt, False)
                self.setBlack(brother, True)
                self.rotate(prt, brother)

            elif lb and rb:
                # case 2: brother is black and two kids are black.
                # conveted to the begin case
                self.setBlack(brother, False)
                chd = prt
                prt = chd.parent
            else:
                if rb:
                    # case 3: brother is black and left kid is red and right child is black
                    # rotate bro to make g w wl wr in one line
                    # uncle's son is nephew, and niece for uncle's daughter
                    nephew = brother.getChild(isLeft)
                    self.setBlack(nephew, True)
                    self.setBlack(brother, False)

                    # brother (not isLeft) rotate
                    self.rotate(brother, nephew)
                    brother = nephew

                # case 4: brother is black and right child is red
                brother.isBlack = prt.isBlack
                self.setBlack(prt, True)
                self.setBlack(brother.getChild(not isLeft), True)

                self.rotate(prt, brother)
                chd = self.root
        self.setBlack(chd, True)
    
    def display(self):
        def getHeight(nd):
            if nd is None:
                return 0
            return max(getHeight(nd.lchild),getHeight(nd.rchild))+1

        def levelVisit(root):
            from collections import deque
            lst = deque([root])
            level = []
            h = getHeight(root)
            ct = lv = 0
            while 1:
                ct += 1
                nd = lst.popleft()
                if ct >= 2**lv:
                    lv += 1
                    if lv > h: break
                    level.append([])
                level[-1].append(str(nd))
                if nd is not None:
                    lst += [nd.lchild, nd.rchild]
                else:
                    lst += [None, None]
            return level

        def addBlank(lines):
            width = 5
            sep = ' ' * width
            n = len(lines)
            for i, oneline in enumerate(lines):
                k = 2**(n - i) - 1
                new = [sep * ((k - 1) // 2)]
                for s in oneline:
                    new.append(s.ljust(width))
                    new.append(sep * k)
                lines[i] = new
            return lines

        lines = levelVisit(self.root)
        lines = addBlank(lines)
        li = [''.join(line) for line in lines]
        length = 10 if li == [] else max(len(i) for i in li) // 2
        begin = '\n' + 'red-black-tree'.rjust(length + 14,
                                              '-') + '-' * (length)
        end = '-' * (length * 2 + 14) + '\n'
        return '\n'.join([begin, *li, end])

    def sort(self, reverse=False):
        ''' return a generator of sorted data'''

        def inOrder(root):
            if root is None: return
            if reverse:
                yield from inOrder(root.rchild)
            else:
                yield from inOrder(root.lchild)
            yield root
            if reverse:
                yield from inOrder(root.lchild)
            else:
                yield from inOrder(root.rchild)

        yield from inOrder(self.root)

    def __str__(self):
        return self.display()


def genNum(n=10):
    nums = []
    for i in range(n):
        while 1:
            d = randint(0, 100)
            if d not in nums:
                nums.append(d)
                break
    return nums


def buildTree(n=10, nums=None, visitor=None):
    if nums is None or nums == []: nums = genNum(n)
    rbtree = RBTree()
    print(f'build a red-black tree using {nums}')
    for i in nums:
        rbtree.insert(i)
        if visitor:
            visitor(rbtree,i)
    return rbtree, nums


def testInsert(nums=None):
    def visitor(t, val):
        print('inserting', val)
        print(t)

    rbtree, nums = buildTree(visitor=visitor, nums=nums)
    print('-' * 5 + 'in-order visit' + '-' * 5)
    for i, j in enumerate(rbtree.sort()):
        print(f'{i+1}: {j}')

def test(nums):
    def visitor(t, val):
        print('inserting', val)
        print(t)

    rbtree = buildTree(visitor=visitor, nums=nums)
    sorted_nodes = []
    for i, j in enumerate(rbtree.sort()):
        sorted_nodes.append(j.val)
        print(f'{i+1}: {j}')

    n1 = int(len(sorted_nodes)/4)
    n2 = int(len(sorted_nodes)/2)
    print(f'deleting {sorted_nodes[n1]}')
    rbtree.delete(sorted_nodes[n1])
    print(rbtree)
    print(f'deleting {sorted_nodes[n2]}')
    rbtree.delete(sorted_nodes[n2])
    print(rbtree)



if __name__ == '__main__':
    #lst = [45, 30, 64, 36, 95, 38, 76, 34, 50, 1]
    #lst = [0, 3, 5, 6, 26, 25, 8, 19, 15, 16, 17]
    #testSuc(lst)
    #n1, n2 = testInsert(lst)
    n = int(input('enter:'))
    nums = [randint(0,100) for i in range(n)]
    test(nums)