import random
import time
import sys 
import os
sys.path.append(os.path.abspath("C:\\Users\\Lenovo\\source\\repos\\AdventOfCode23\\binary_tree"))
from binary_tree import BalancedBinaryTree

b = BalancedBinaryTree(lambda x, y: x - y)

def assert_count(node):
    left_correct, left_count = (True, 0) if node.left is None else assert_count(node.left)
    right_correct, right_count = (True, 0) if node.right is None else assert_count(node.right)

    correct_count = left_correct and right_correct and node.count == left_count + right_count + 1
    is_balanced = abs(left_count - right_count) <= 1

    if not is_balanced:
        print('warning: ', abs(left_count - right_count))

    return correct_count, left_count + right_count + 1

start = time.time()
for i in range(5000):
    b.add(random.randint(1, 1000))
    #correct, count = assert_count(b.root)
    #if not correct:
    #    b.print()
    #    break

end = time.time()
print(end - start)