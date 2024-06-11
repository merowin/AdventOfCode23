import re
import random

import sys 
import os
sys.path.append(os.path.abspath("C:\\Users\\Lenovo\\source\\repos\\AdventOfCode23\\binary_tree"))
from binary_tree import BalancedBinaryTree

class Hand:
   def __init__(self, cards: str, bid: int):
      self.cards = cards
      self.bid = bid
      self.type = self.determineType()
      self.cardValues = self.determineCardValues()

   # five of a kind -> 6
   # four of a kind -> 5
   # full house -> 4
   # three of a kind -> 3
   # two pair -> 2
   # one pair -> 1
   # high card -> 0
   def determineType(self) -> int:
      cardCounts = [0] * 12
      jokerCount = 0
      for c in self.cards:
         value = cardsMap.get(c)
         if value == 0:
            jokerCount += 1
         else:
            cardCounts[cardsMap.get(c) - 1] += 1
      
      cardCounts.sort(reverse=True)
      highestCount = cardCounts[0] + jokerCount
      secondHighestCount = cardCounts[1]

      if highestCount == 5:
         return 6
      
      if highestCount == 4:
         return 5
      
      if highestCount == 3:
         return 4 if secondHighestCount == 2 else 3
      
      if highestCount == 2:
         return 2 if secondHighestCount == 2 else 1
      
      return 0
   
   def determineCardValues(self) -> [int]:
      return list(map(lambda c: cardsMap.get(c), self.cards))

   
def handsComparer(hand1: Hand, hand2: Hand) -> int:
   if hand1.type < hand2.type:
      return -1
   
   if hand1.type > hand2.type:
      return 1
   
   for i in range(5):
      c1 = hand1.cardValues[i]
      c2 = hand2.cardValues[i]

      if c1 < c2:
         return -1
      
      if c1 > c2:
         return 1

   return 0

cardsMap = {
   'A': 12,
   'K': 11,
   'Q': 10,
   'T': 9,
   '9': 8,
   '8': 7,
   '7': 6,
   '6': 5,
   '5': 4,
   '4': 3,
   '3': 2,
   '2': 1,
   'J': 0,
}

sum = 0

binaryTree = BalancedBinaryTree(handsComparer)

with open('input.txt', encoding="utf-8") as f:

    for line in f.readlines():
        if (line == ' '):
           # last line
           break

        cards = line.split(' ')[0]
        bid = int(line.split(' ')[1].split('\n')[0])
        binaryTree.add(Hand(cards, bid))

orderedHands = binaryTree.getOrderedData()
for i in range(len(orderedHands)):
   hand = orderedHands[i]
   #print(hand.cards, hand.bid, sep=' ')
   sum += (i + 1) * hand.bid

print(sum)