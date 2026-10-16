import unittest
from raven.graphs import PotentialEdge
from raven.portfolio import exhaustive,utility
from raven.pruning import screen

class Portfolio(unittest.TestCase):
    def setUp(self):
        self.a=('a','constraints');self.b=('b','constraints')
        self.edges=[PotentialEdge('a','b',1,frozenset([self.a,self.b]))]
    def test_complementarity(self):
        self.assertEqual(utility([self.a],[],self.edges),0)
        self.assertEqual(utility([self.b],[],self.edges),0)
        self.assertEqual(utility([self.a,self.b],[],self.edges),1)
        self.assertEqual(len(exhaustive([self.a,self.b],6,[],self.edges)[0]),2)
    def test_budget(self):
        self.assertEqual(exhaustive([self.a,self.b],3,[],self.edges)[0],())
    def test_zero_budget(self):self.assertEqual(exhaustive([self.a],0,[],self.edges)[0],())
    def test_group_pruning(self):self.assertEqual(screen([self.a,self.b],self.edges,2),[self.a,self.b])
    def test_search_cap(self):self.assertFalse(exhaustive([self.a,self.b],6,[],self.edges,limit=1)[3])
    def test_deterministic(self):self.assertEqual(exhaustive([self.a,self.b],6,[],self.edges),exhaustive([self.a,self.b],6,[],self.edges))
