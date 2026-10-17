"""Research API checks, not evidence that these methods are deployed."""
import copy
import itertools
import math
import random
import unittest
from unittest.mock import patch
from raven.graphs import ConfirmedEdge as E, PotentialEdge as P
from raven.matching import allocate, greedy
from raven.portfolio import exhaustive, utility
from raven.pruning import screen
from raven.probabilities import features,predict,sigmoid,assets
from tests.hardening_fixtures import compatible_sim,set_field


def oracle_matching(edges):
    weights={}
    for e in edges:
        if e.a!=e.b:
            key=tuple(sorted((e.a,e.b))); weights[key]=max(weights.get(key,0),e.weight)
    def solve(nodes):
        if not nodes:return 0
        a,*rest=nodes
        return max([solve(rest)]+[w+solve([i for i in rest if i!=b]) for b in rest if (w:=weights.get(tuple(sorted((a,b))),0))>0])
    return solve(sorted({i for pair in weights for i in pair}))


class HardeningMatching(unittest.TestCase):
    def check(self,edges):
        out=allocate(edges); flattened=[i for pair in out for i in pair]
        self.assertEqual(len(flattened),len(set(flattened)))
        weights={}
        for e in edges:
            key=tuple(sorted((e.a,e.b))); weights[key]=max(weights.get(key,0),e.weight)
        self.assertAlmostEqual(sum(weights[tuple(p)] for p in out),oracle_matching(edges),places=8)

    def test_graph_families_integer_optimality(self):
        graphs=[[],[('a','b')],[('a','b'),('b','c'),('c','a')],
                [('a','b'),('b','c'),('c','d'),('d','a')],
                [('a','b'),('b','c'),('c','d'),('d','e'),('e','a')],
                [('a',b) for b in 'bcdef'],list(itertools.combinations('abcdef',2)),
                [(a,b) for a in 'abc' for b in 'def'],[('a','b'),('c','d'),('e','f')]]
        for graph in graphs:
            for weights in ('equal','asymmetric'):
                self.check([E(a,b,1 if weights=='equal' else (i+1)**3) for i,(a,b) in enumerate(graph)])

    def test_seeded_oracle_and_zero_negative_edges(self):
        rng=random.Random(24031)
        for _ in range(120):
            self.check([E(a,b,rng.choice([-3,0,1,2,10,100000])) for a,b in itertools.combinations('abcdefg',2) if rng.random()<.5])

    def test_reversed_duplicate_weights(self):
        # Repeated candidates denote one undirected edge; retain its best weight.
        self.check([E('a','b',10),E('a','b',1),E('b','a',2),E('a','c',3),E('b','d',3)])

    def test_tiny_and_large_finite_weights(self):
        for w in (1e-15,1e-9,1.0,1e100):
            self.assertEqual(allocate([E('a','b',w)]),[['a','b']])
        self.assertEqual(allocate([E('a','b',0),E('c','d',-1)]),[])

    def test_greedy_behavior_and_oversize_fallback(self):
        edges=[E('a','b',9),E('a','c',8),E('b','d',8)]
        self.assertEqual(allocate(edges,'greedy'),[['a','b']])
        self.assertEqual(oracle_matching(edges),16) # no global-optimality claim for greedy
        edges=[E(str(i),str(i+1),1) for i in range(221)]
        with patch('raven.vendor.blossom.max_weight_matching',side_effect=AssertionError('must not invoke')):
            self.assertEqual(allocate(edges),greedy(edges))


class HardeningPortfolio(unittest.TestCase):
    def test_independent_subset_oracle_and_regret(self):
        rng=random.Random(24041)
        for n in (0,1,2,5,11,12,13):
            qs=[(str(i),'constraints') for i in range(n)]
            potential=[P(str(i),str(i+1),rng.random(),frozenset(qs[i:i+2])) for i in range(max(0,n-1))]
            for budget in (0,2,3,6,12,3*n):
                if n>5 and budget>12:continue
                candidates=[combo for k in range(min(n,budget//3)+1) for combo in itertools.combinations(qs,k)]
                best=max(utility(x,[],potential) for x in candidates)
                selected,value,count,exact=exhaustive(qs,budget,[],potential)
                self.assertTrue(exact);self.assertAlmostEqual(value,best)
                self.assertLessEqual(3*len(selected),budget)
                for limit in (0,1,2,4,12):
                    kept=screen(qs,potential,limit)
                    self.assertLessEqual(len(kept),limit)
                    self.assertTrue(set(kept)<=set(qs))
                    pruned=exhaustive(kept,budget,[],potential)[1]
                    self.assertGreaterEqual(value-pruned,-1e-12)
                    self.assertEqual(kept,screen(qs,potential,limit))

    def test_shortlist_never_invents_candidates(self):
        q=('a','constraints'); absent=('absent','constraints')
        p=[P('a','absent',1,frozenset((q,absent)))]
        self.assertEqual(screen([q],p,12),[q])

    def test_complementary_redundant_equal_and_low_value(self):
        qs=[(x,'constraints') for x in 'abcd']
        edges=[P('a','b',1,frozenset(qs[:2])),P('c','d',1,frozenset(qs[2:]))]
        self.assertEqual(exhaustive(qs,3,[],edges)[0],())
        self.assertEqual(exhaustive(qs,6,[],edges)[1],1)
        self.assertEqual(exhaustive(qs,12,[],edges)[1],2)
        self.assertEqual(exhaustive(qs,12,[],[])[0],())
        self.assertEqual(exhaustive(qs,12,[],edges,limit=0)[3],False)
        for w in (0,1e-15,1e-6,1e100):
            value=utility(qs,[],[P('a','b',w,frozenset(qs[:2]))])
            self.assertTrue(math.isfinite(value)); self.assertEqual(value,w)


class HardeningProbabilities(unittest.TestCase):
    def test_cold_start_declined_unseen_and_extreme_logits(self):
        a,b=compatible_sim().observe()['members']
        for status in ('observed','not_asked','declined'):
            for m in (a,b):
                for key in ('relationship_goal','lifestyle','conversations'):
                    set_field(m,key,'unseen' if status=='observed' else None,status)
            for target in ('directional','joint','date','msmi'):
                for calibrated in (True,False):
                    p=predict(a,b,59,target,calibrated=calibrated)
                    self.assertTrue(math.isfinite(p));self.assertTrue(0<p<1)
                    if target!='directional':self.assertEqual(p,predict(b,a,59,target,calibrated=calibrated))
        for x in (-1e300,-1000,0,1000,1e300):self.assertTrue(0<sigmoid(x)<1)

    def test_immutable_model_and_no_hidden_features(self):
        a,b=compatible_sim().observe()['members']; original=copy.deepcopy(assets()); x=features(a,b)
        a.update(truth={'secret':1},exit_day=-1,bias=100,response_rate=0,member_id='irrelevant')
        self.assertEqual(features(a,b),x)
        predict(a,b);self.assertEqual(assets(),original)

    def test_fitting_empty_single_class_and_imbalance(self):
        try:
            import numpy as np
            from experiments.train import logistic_fit,fit
        except ImportError:
            self.skipTest('Training-only NumPy is not an inference dependency')
        width=len(features(*compatible_sim().observe()['members']))
        for labels in ([],[0],[1],[0]*20,[1]*20,[0]*999+[1]):
            x=np.ones((len(labels),width)); weights,prior=logistic_fit(x,labels)
            self.assertEqual(len(weights),width);self.assertTrue(all(math.isfinite(w) for w in weights))
            self.assertTrue(0<prior<1)
        empty=dict(rows=[],gates=[],zones={},arrivals={},episodes=0)
        model=fit(empty,empty)
        self.assertTrue(all(math.isfinite(w) for t in model['targets'].values() for w in t['weights']))
        self.assertEqual(model['future']['arrivals'],{})

    def test_directional_joint_labels_and_pre_action_features(self):
        try:
            from experiments import train
        except ImportError:
            self.skipTest('Training-only NumPy is not an inference dependency')
        from kit import Simulator
        snapshots={}; instances=[]
        class RecordingSimulator(Simulator):
            def __init__(self,world):
                super().__init__(world);instances.append(self)
            def advance(self,pairs):
                people={m['member_id']:m for m in self.observe()['members']}
                for a,b in pairs:
                    snapshots[(a,b,self.day)]=(features(people[a],people[b],self.day),features(people[b],people[a],self.day))
                super().advance(pairs)
        with patch.object(train,'Simulator',RecordingSimulator),patch('builtins.print'):
            data=train.collect([24051],['delayed'])
        self.assertTrue(data['rows'])
        sim=instances[0]; intros={frozenset((i['user_a'],i['user_b'])):i for i in sim.introductions}
        for row in data['rows']:
            self.assertEqual((row['x'],row['xr']),snapshots[(row['a'],row['b'],row['day'])])
            intro=intros[frozenset((row['a'],row['b']))]
            events=[e for e in sim.receive_feedback() if e['introduction_id']==intro['introduction_id']]
            yes={e['member_id'] for e in events if e['event']=='introduction_response' and e['value']=='yes'}
            self.assertEqual(row['directional'],int(row['a'] in yes))
            self.assertEqual(row['directional_reverse'],int(row['b'] in yes))
            self.assertEqual(row['joint'],int({row['a'],row['b']}<=yes))
            self.assertEqual(row['matured_day'],100)
            dates=[e for e in events if e['event']=='date_happened' and e['value'] is True]
            seconds=[e for e in events if e['event']=='second_meeting_intention']
            expected=bool(dates) and dates[0]['occurred_day']-row['day']<=30 and len(seconds)==2 and all(
                e['value']=='yes' and e['occurred_day']-dates[0]['occurred_day']<=3 for e in seconds)
            self.assertEqual(row['msmi'],int(expected))
        # These are matured recorded-event targets, never preference labels for absent dates.
