import unittest
from kit import generate,Simulator
from raven.protocol import decide
from raven.config import config
from raven.constraints import eligibility,Status

class Temporal(unittest.TestCase):
    def test_feedback_no_future(self):
        sim=Simulator(generate(15002,30))
        for day in range(8):
            request={'phase':'ask','state':sim.observe(),'memory':{}}
            sim.resolve_asks(decide(request,'joint')['asks'])
            state=sim.observe();action=decide({'phase':'match','state':state},'joint')['pairs']
            people={m['member_id']:m for m in state['members']}
            for a,b in action:self.assertEqual(eligibility(people[a],people[b]),Status.CONFIRMED_FEASIBLE)
            sim.advance(action)
            self.assertTrue(all(e['observed_day']<=sim.day for e in sim.receive_feedback()))
    def test_deterministic_and_no_mutation(self):
        import copy
        state=Simulator(generate(15003,40)).observe();request={'phase':'ask','state':state,'memory':None}
        saved=copy.deepcopy(request)
        self.assertEqual(decide(request,'joint'),decide(request,'joint'))
        self.assertEqual(request,saved)
