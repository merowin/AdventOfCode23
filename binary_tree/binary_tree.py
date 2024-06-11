# node class for a balanced binary tree
# should satisfy:
#
# comparer(self.data, self.left.data) >= 0
# comparer(self.data, self.right.data) >= 0
#
# for any leftNode in the left subtree, and any rightNode in the right subtree:
# comparer(leftNode.data, rightNode.data) <= 0
#
# number of nodes in left and right subtree differ by at most one

class BalancedBinaryTreeNode:
  def __init__(self, parentTree, data) -> None:
    self.left = None
    self.right = None
    self.data = data
    self.count = 1
    self.parentTree = parentTree

  def popMinOfSubtree(self) -> any:
    self.count -= 1

    if not self.left is None:
      if self.left.left is None and self.left.right is None:
        temp = self.left
        self.left = None
        return temp
      
      return self.left.popMinOfSubtree()
    
    if not self.right is None:
      if self.right.left is None and self.right.right is None:
        temp = self.right
        self.right = None
        return temp
      
      return self.right.popMinOfSubtree()
    
    print('warn: pop reached unreachable code')
    # revert count change
    self.count += 1
    return self

  # should only be called when subtrees are left-heavy
  # moves self.left to the right subtree
  # re-connects the two parts on the left
  def rightShift(self) -> None:
    if self.left is None:
      return
    
    left_temp = self.left
    left_left_temp = self.left.left
    left_right_temp = self.left.right

    # cut out self.left
    left_temp.left = None
    left_temp.right = None
    left_temp.count = 1
    self.left = None

    # reconnect left subtree
    if not left_left_temp is None:
      if not left_right_temp is None:
        left_right_temp.addNode(left_left_temp)

    self.left = left_right_temp if not left_right_temp is None else left_left_temp

    # add the cut-out node to right subtree
    if (self.right is None):
      self.right = left_temp

    else:
      self.right.addNode(left_temp)

  # should only be called when subtrees are right-heavy
  def leftShift(self) -> None:
    if self.right is None:
      return
    
    right_min = self.right.popMinOfSubtree()

    if self.left is None:
      self.left = right_min
    else:
      self.left.addNode(right_min)

  def addNode(self, newNode):
      if self.parentTree.comparer(self.data, newNode.data) < 0:
        # update max in this subtree by swapping
        self.data, newNode.data = newNode.data, self.data
      
      self.count += newNode.count

      if (not self.right is None) and self.parentTree.comparer(newNode.data, self.right.data) > 0:
          self.right.addNode(newNode)
          return
      
      if self.left is None:
        self.left = newNode
        return

      if self.parentTree.comparer(self.left.data, newNode.data) >= 0:
        self.left.addNode(newNode)
        return

      elif self.right is None:
        self.right = newNode
        return

      self.right.addNode(newNode)

  def addNodeAndEnsureBalance(self, newNode):
    self.addNode(newNode)
    self.ensureBalance()

  def ensureBalance(self) -> None:
    while (0 if self.left is None else self.left.count) > (0 if self.right is None else self.right.count) + 1:
      self.rightShift()

    while (0 if self.left is None else self.left.count) < (0 if self.right is None else self.right.count) - 1:
      self.leftShift()

    if not self.left is None:
      self.left.ensureBalance()
    
    if not self.right is None:
      self.right.ensureBalance()

  def getOrderedData(self) -> [any]:
    left = self.left.getOrderedData() if not self.left is None else []
    right = self.right.getOrderedData() if not self.right is None else []
    return left + right + [self.data]

  def print(self) -> None:
    print('****************')
    print('node data:', self.data, 'count:', self.count, 'left node data:',
          'none' if (self.left is None) else self.left.data, 'right node data:',
          'none' if (self.right is None) else self.right.data, sep=' | ')
    if not self.left is None:
      self.left.print()
    if not self.right is None:
      self.right.print()

class BalancedBinaryTree:
  def __init__(self, comparer) -> None:
    self.root = None

    # comparer(node1.data, node2.data) < 0 represents the order node1.data < node2.data
    # comparer(node1.data, node2.data) = 0 represents the order node1.data = node2.data
    # comparer(node1.data, node2.data) > 0 represents the order node1.data > node2.data
    self.comparer = comparer

  def addNode(self, newNode: BalancedBinaryTreeNode):
    if (self.root is None):
      self.root = newNode
    else:
      self.root.addNodeAndEnsureBalance(newNode)

  def add(self, data) -> None:
    self.addNode(BalancedBinaryTreeNode(self, data))

  def getOrderedData(self) -> [any]:
    return [] if self.root is None else self.root.getOrderedData()
  
  def print(self) -> None:
    print('***********')
    print('print tree:')
    if self.root is None:
      print('no nodes in tree')
      return
    self.root.print()