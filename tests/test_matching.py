import itertools
import random
import unittest
from raven.graphs import ConfirmedEdge,PotentialEdge
from raven.matching import allocate,greedy

def brute(edges):
    if not edges:return 0
    first,*rest=edges
    return max(brute(rest),first.weight+brute([e for e in rest if not {e.a,e.b}&{first.a,first.b}]))

class Matching(unittest.TestCase):
    def test_empty(self):self.assertEqual(allocate([]),[])
    def test_negative(self):self.assertEqual(allocate([ConfirmedEdge('a','b',-1)]),[])
    def test_one(self):self.assertEqual(allocate([ConfirmedEdge('a','b',1)]),[['a','b']])
    def test_counterexample(self):
        edges=[ConfirmedEdge('a','b',.9),ConfirmedEdge('c','d',.05),ConfirmedEdge('a','d',.65),ConfirmedEdge('b','c',.65)]
        self.assertEqual(allocate(edges),[['a','d'],['b','c']])
    def test_potential_rejected(self):
        with self.assertRaises(TypeError):allocate([PotentialEdge('a','b',1,frozenset())])
    def test_random_bruteforce_and_odd_cycles(self):
        rng=random.Random(19)
        for n in range(2,8):
            for _ in range(25):
                edges=[ConfirmedEdge(str(a),str(b),rng.randint(1,20)) for a,b in itertools.combinations(range(n),2) if rng.random()<.5]
                weights={(e.a,e.b):e.weight for e in edges}
                self.assertEqual(sum(weights[tuple(p)] for p in allocate(edges)),brute(edges))
    def test_against_networkx(self):
        import networkx as nx
        rng=random.Random(72)
        for _ in range(20):
            edges=[ConfirmedEdge(str(a),str(b),rng.randint(1,100)) for a,b in itertools.combinations(range(30),2) if rng.random()<.4]
            graph=nx.Graph();graph.add_weighted_edges_from((e.a,e.b,e.weight) for e in edges)
            weights={tuple(sorted((e.a,e.b))):e.weight for e in edges}
            own=sum(weights[tuple(p)] for p in allocate(edges))
            ref=sum(graph[a][b]['weight'] for a,b in nx.max_weight_matching(graph))
            self.assertEqual(own,ref)
