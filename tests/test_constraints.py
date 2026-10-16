import copy
import itertools
import random
import unittest
from kit import eligibility as oracle,generate,Simulator
from raven.constraints import HARD,Status,eligibility,recoverable

def pair():
    a,b=Simulator(generate(42,2)).observe().get('members',[]),None
    people=generate(43,2)['members']
    fields=dict(age_min=18,age_max=65,who_to_meet=['woman','man','non_binary'],
                relationship_structure='monogamous',smoking='no',partner_smoking='any',has_children=False,
                partner_children='any',wants_children='unsure',acceptable_zones=['z'],schedule=['weekend_day'])
    for p in people:
        p['fields']=fields.copy();p['zone']='z';p['available']=True
        p['field_status']={k:'observed' for k in HARD}
    return people

class Constraints(unittest.TestCase):
    def test_valid(self): self.assertEqual(eligibility(*pair()),Status.CONFIRMED_FEASIBLE)
    def test_all_hard_missingness_combinations(self):
        # Exhaust all 2^11 presence masks independently at each endpoint.
        for endpoint in (0,1):
            for mask in range(1<<len(HARD)):
                a,b=pair();m=(a,b)[endpoint]
                for index,k in enumerate(HARD):
                    if mask&(1<<index):m['fields'][k]=None
                self.assertEqual(eligibility(a,b).value,oracle(a,b)['status'])
    def test_random_differential(self):
        rng=random.Random(19)
        for seed in range(10):
            members=generate(seed,40)['members']
            for a,b in itertools.combinations(members,2):
                a,b=copy.deepcopy(a),copy.deepcopy(b)
                for m in (a,b):
                    for k in HARD:
                        if rng.random()<.5:m['fields'][k]=m['truth'][k]
                self.assertEqual(eligibility(a,b).value,oracle(a,b)['status'])
                self.assertEqual(eligibility(a,b),eligibility(b,a))
    def test_blocker_priority(self):
        a,b=pair();a['fields']['age_max']=18;b['fields']['schedule']=None
        self.assertEqual(eligibility(a,b),Status.CONFIRMED_INFEASIBLE)
    def test_each_blocker(self):
        changes=[('age_min',65),('age_max',18),('who_to_meet',[]),('acceptable_zones',['other']),
                 ('relationship_structure','non_monogamous'),('schedule',['weekday_evening'])]
        for endpoint in (0,1):
            for key,value in changes:
                a,b=pair();(a,b)[endpoint]['fields'][key]=value
                self.assertEqual(eligibility(a,b),Status.CONFIRMED_INFEASIBLE)
    def test_children_and_smoking(self):
        for smoker in ('occasionally','yes'):
            a,b=pair();a['fields']['partner_smoking']='no_smoking';b['fields']['smoking']=smoker
            self.assertEqual(eligibility(a,b),Status.CONFIRMED_INFEASIBLE)
        a,b=pair();a['fields']['partner_children']='no_children';b['fields']['has_children']=True
        self.assertEqual(eligibility(a,b),Status.CONFIRMED_INFEASIBLE)
        a,b=pair();a['fields']['wants_children']='yes';b['fields']['wants_children']='no'
        self.assertEqual(eligibility(a,b),Status.CONFIRMED_INFEASIBLE)
    def test_declined(self):
        a,b=pair();a['fields']['schedule']=None;a['field_status']['schedule']='declined'
        self.assertFalse(recoverable(a));self.assertEqual(eligibility(a,b),Status.UNKNOWN_PENDING_CLARIFICATION)
    def test_identity_pool_adult(self):
        for key,value in [('member_id',None),('pool_id','other'),('age',17)]:
            a,b=pair();a[key]=b[key] if value is None else value
            self.assertEqual(eligibility(a,b),Status.CONFIRMED_INFEASIBLE)
