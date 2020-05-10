
from functools import total_ordering
from random import randint, shuffle


@total_ordering
class node:
    def __init__(self, val, left=None, right=None, isBlack=False):
        self.val = val
        self.left = left
        self.right = right
        self.parent = None
        self.isBlack = isBlack

    def __lt__(self, nd):
        return self.val < nd.val

    def __eq__(self, nd):
        return nd is not None and self.val == nd.val

    def setChild(self, nd, isLeft):
        if isLeft: self.left = nd
        else: self.right = nd
        if nd is not None: nd.parent = self

    def getChild(self, isLeft):
        if isLeft: return self.left
        else: return self.right

    def __bool__(self):
        return self.val is not None

    def __str__(self):
        color = 'B' if self.isBlack else 'R'
        val = '-' if self.parent == None else self.parent.val
        return f'{color}-{self.val}'

    def __repr__(self):
        return f'node({self.val},isBlack={self.isBlack})'


class redBlackTree:
    def __init__(self, unique=False):
        '''if unique is True, all node'vals are unique, else there may be equal vals'''
        self.root = None
        self.unique = unique

    @staticmethod
    def checkBlack(nd):
        return nd is None or nd.isBlack

    @staticmethod
    def setBlack(nd, isBlack):
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

    def getSuccessor(self, nd):
        if nd:
            if nd.right:
                nd = nd.right
                while nd.left:
                    nd = nd.left
                return nd
            else:
                while nd.parent is not None and nd.parent.right is nd:
                    nd = nd.parent
                return None if nd is self.root else nd.parent

    def rotate(self, parent, child):
        '''rotate parent with the center of child'''
        if self.root is parent:
            self.setRoot(child)
        else:
            parent.parent.setChild(child, parent.parent.left is parent)
        isLeftchild = parent.left is child
        parent.setChild(child.getChild(not isLeftchild), isLeftchild)
        child.setChild(parent, not isLeftchild)

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
                child = parent.getChild(isLeft)
                if child is None:
                    parent.setChild(nd, isLeft)
                    break
                else:
                    parent = child
            self.fixUpInsert(parent, nd)

    def fixUpInsert(self, parent, nd):
        ''' adjust color and level,  there are two red nodes: the new one and its parent'''
        while not self.checkBlack(parent):
            grand = parent.parent
            isLeftparent = grand.left is parent
            uncle = grand.getChild(not isLeftparent)
            if not self.checkBlack(uncle):
                # case 1:  new node's uncle is red
                self.setBlack(grand, False)
                self.setBlack(grand.left, True)
                self.setBlack(grand.right, True)
                nd = grand
                parent = nd.parent
            else:
                # case 2: new node's uncle is black(including nil leaf)
                isLeftNode = parent.left is nd
                if isLeftNode ^ isLeftparent:
                    # case 2.1 the new node is inserted in left-right or right-left form
                    self.rotate(parent, nd)  #parent rotate
                    nd, parent = parent, nd
                # case 2.2 the new node is inserted in left-left or right-right form
                self.setBlack(grand, False)
                self.setBlack(parent, True)
                self.rotate(grand, parent)
        self.setBlack(self.root, True)

    def copyNode(self, src, des):
        des.val = src.val

    def delete(self, val):
        '''delete node in a binary search tree'''
        if isinstance(val, node): val = val.val
        nd = self.find(val)
        if nd is None: return
        self._delete(nd)

    def _delete(self, nd):
        y = None
        if nd.left and nd.right:
            y = self.getSuccessor(nd)
        else:
            y = nd
        py = y.parent
        x = y.left if y.left else y.right
        if py is None:
            self.setRoot(x)
        else:
            py.setChild(x, py.left is y)
        if y != nd:
            self.copyNode(y, nd)
        if self.checkBlack(y): self.fixupDelete(py, x)

    def fixupDelete(self, parent, child):
        ''' adjust colors and rotate '''
        while self.root != child and self.checkBlack(child):
            isLeft = parent.left is child
            brother = parent.getChild(not isLeft)
            # brother is black
            lb = self.checkBlack(brother.getChild(isLeft))
            rb = self.checkBlack(brother.getChild(not isLeft))
            if not self.checkBlack(brother):
                # case 1: brother is red.   converted to  case 2,3,4

                self.setBlack(parent, False)
                self.setBlack(brother, True)
                self.rotate(parent, brother)

            elif lb and rb:
                # case 2: brother is black and two kids are black.
                # conveted to the begin case
                self.setBlack(brother, False)
                child = parent
                parent = child.parent
            else:
                if rb:
                    # case 3: brother is black and left kid is red and right child is black
                    # rotate bro to make g w wl wr in one line
                    nephew = brother.getChild(isLeft)
                    self.setBlack(nephew, True)
                    self.setBlack(brother, False)

                    # brother (not isLeft) rotate
                    self.rotate(brother, nephew)
                    brother = nephew

                # case 4: brother is black and right child is red
                brother.isBlack = parent.isBlack
                self.setBlack(parent, True)
                self.setBlack(brother.getChild(not isLeft), True)

                self.rotate(parent, brother)
                child = self.root
        self.setBlack(child, True)

    def sort(self, reverse=False):
        ''' return a generator of sorted data'''

        def inOrder(root):
            if root is None: return
            if reverse:
                yield from inOrder(root.right)
            else:
                yield from inOrder(root.left)
            yield root
            if reverse:
                yield from inOrder(root.left)
            else:
                yield from inOrder(root.right)

        yield from inOrder(self.root)

    def display(self):
        def getHeight(nd):
            if nd is None: return 0
            return max(getHeight(nd.left), getHeight(nd.right)) + 1

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
                    lst += [nd.left, nd.right]
                else:
                    lst += [None, None]
            return level

        def addBlank(lines):
            width = int(float(len(str(self.root)))/2)
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
        #length = 10 if li == [] else max(len(i) for i in li) // 2
        begin = '\n' + 'RBT'.rjust(90,
                                              '-') + '-' * (90)
        end = '-' * (180) + '\n'
        return '\n'.join([begin, *li, end])

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
    rbtree = redBlackTree()
    print(f'build a red-black tree using {nums}')
    for i in nums:
        rbtree.insert(node(i))
        #print(rbtree)
        if visitor:
            visitor(rbtree, i)
    return rbtree


def testInsert(nums=None):
    def visitor(t, val):
        print('inserting', val)
        print(t)

    rbtree = buildTree(visitor=visitor, nums=nums)
    print('in-order visit:')
    sorted_nodes=[]
    for i, j in enumerate(rbtree.sort()):
        sorted_nodes.append(j.val)
        print(f'{i+1}: {j}')
    
    return rbtree
    
    


def testSuc(nums=None):
    rbtree = buildTree(nums=nums)
    for i in rbtree.sort():
        print(f'{i}\'s suc is {rbtree.getSuccessor(i)}')


def testDelete(nums=None):
    rbtree = buildTree(nums=nums)
    print(rbtree)
    for i in sorted(nums):
        print(f'deleting {i}')
        rbtree.delete(i)
        print(rbtree)

def test(nums):
    def visitor(t, val):
        print('inserting', val)
        print(t)

    rbtree = buildTree(visitor=visitor, nums=nums)
    sorted_nodes=[]
    for i, j in enumerate(rbtree.sort()):
        sorted_nodes.append(j.val)
        print(f'{i+1}: {j}')
    print('\n')

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
    nums = [randint(0,500) for i in range(n)]
    test(nums)