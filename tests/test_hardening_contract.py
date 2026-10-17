"""Valid public observations and independent official action oracles.

Malformed observations are confined to explicitly named defensive tests elsewhere.
"""
import copy
import itertools
import json
import random
import unittest
from unittest.mock import patch
from evaluate import validate_response, VARIANTS
from kit import Simulator, generate, eligibility as oracle, HARD, SOFT, baseline_asks, baseline_match
from raven.constraints import eligibility
from raven.protocol import decide
from raven.validation import sanitize
from tests.hardening_fixtures import compatible_sim, request, set_field


class HardeningContract(unittest.TestCase):
    def assert_action(self, state, phase, response):
        validate_response(response, phase)
        json.dumps(response, allow_nan=False)
        people = {m['member_id']: m for m in state['members']}
        if phase == 'ask':
            seen = set(); cost = 0
            for a in response['asks']:
                self.assertIn(a['field'], ['constraints'] + SOFT)
                self.assertTrue(people[a['member_id']]['available'])
                key = (a['member_id'], a['field'])
                self.assertNotIn(key, seen); seen.add(key)
                cost += 3 if a['field'] == 'constraints' else 1
            self.assertLessEqual(cost, state['ask_budget_remaining'])
        else:
            used = set()
            past = {frozenset((i['user_a'], i['user_b'])) for i in state['introductions']}
            for a, b in response['pairs']:
                self.assertNotIn(a, used); self.assertNotIn(b, used)
                self.assertNotEqual(a, b); used.update((a, b))
                self.assertTrue(people[a]['available'] and people[b]['available'])
                self.assertNotIn(frozenset((a, b)), past)
                self.assertEqual(oracle(people[a], people[b])['status'], 'feasible')

    def test_pool_sizes_and_graph_extremes(self):
        for n in (0, 1, 2, 3, 4, 9, 40, 220, 221):
            for unknown in (False, True):
                sim = compatible_sim(n, unknown=unknown)
                for phase in ('ask', 'match'):
                    state = sim.observe(); out = decide(request(state, phase))
                    self.assert_action(state, phase, out)
                    (sim.resolve_asks if phase == 'ask' else sim.advance)(out['asks' if phase == 'ask' else 'pairs'])
        state = compatible_sim(12).observe()
        for m in state['members']:
            set_field(m, 'who_to_meet', [next(g for g in ('woman','man','non_binary') if g != m['gender'])])
            set_field(m, 'acceptable_zones', ['unoccupied_zone'])
        self.assertEqual(decide(request(state))['pairs'], [])

    def test_each_hard_rule_reciprocally_and_blocker_priority(self):
        for endpoint in (0, 1):
            for missing in (False, True):
                for rule in ('age_min','age_max','who_to_meet','acceptable_zones',
                             'relationship_structure','schedule','smoking','children','wants_children'):
                    state = compatible_sim().observe(); a, b = state['members'][endpoint], state['members'][1-endpoint]
                    values = {'age_min': b['age']+1, 'age_max': b['age']-1,
                              'who_to_meet': [g for g in ('woman','man','non_binary') if g != b['gender']],
                              'acceptable_zones': ['other'], 'relationship_structure':'non_monogamous',
                              'schedule':['weekday_evening']}
                    if rule in values: set_field(a, rule, values[rule])
                    elif rule == 'smoking':
                        set_field(a,'partner_smoking','no_smoking'); set_field(b,'smoking','occasionally')
                    elif rule == 'children':
                        set_field(a,'partner_children','no_children'); set_field(b,'has_children',True)
                    else:
                        set_field(a,'wants_children','yes'); set_field(b,'wants_children','no')
                    if missing: set_field(a, 'has_children', None)
                    with self.subTest(endpoint=endpoint, rule=rule, missing=missing):
                        self.assertEqual(oracle(a,b)['status'], 'infeasible')
                        self.assertEqual(eligibility(a,b).value, oracle(a,b)['status'])
                        self.assertEqual(decide(request(state))['pairs'], [])

    def test_unknown_declined_and_newly_disclosed(self):
        for field in HARD:
            for endpoints in ((0,), (1,), (0,1)):
                for status in ('not_asked', 'declined'):
                    sim = compatible_sim(); state = sim.observe()
                    for i in endpoints: set_field(state['members'][i], field, None, status)
                    self.assertEqual(oracle(*state['members'])['status'], 'needs_clarification')
                    self.assertEqual(decide(request(state))['pairs'], [])
        sim = compatible_sim(2, unknown=True)
        self.assertEqual(decide(request(sim.observe()))['pairs'], [])
        sim.resolve_asks([{'member_id': i, 'field':'constraints'} for i in sim.members])
        self.assertEqual(len(decide(request(sim.observe()))['pairs']), 1)
        sim = compatible_sim(2, unknown=True)
        next(iter(sim.members.values()))['truth']['acceptable_zones'] = ['elsewhere']
        sim.resolve_asks([{'member_id': i,'field':'constraints'} for i in sim.members])
        self.assertEqual(decide(request(sim.observe()))['pairs'], [])

    def test_boundaries_and_unknown_soft(self):
        state = compatible_sim().observe(); a,b = state['members']
        for m, other in ((a,b),(b,a)):
            set_field(m,'age_min',other['age']); set_field(m,'age_max',other['age'])
            for k in SOFT: set_field(m,k,None,'declined')
        self.assertEqual(oracle(a,b)['status'], 'feasible')
        self.assertEqual(len(decide(request(state))['pairs']),1)
        # Unicode opaque pool/zone labels are valid; member IDs remain syn_ + hex.
        for m in (a,b):
            m['pool_id']='synthetic_தமிழ்'; m['zone']='区域'; set_field(m,'acceptable_zones',['区域'])
        self.assertEqual(len(decide(request(state))['pairs']),1)

    def test_budget_and_official_repeat_semantics(self):
        for budget in range(13):
            sim=compatible_sim(20,unknown=True); sim.ask_spent=12-budget
            out=decide(request(sim.observe(),'ask'))
            self.assertEqual(len(out['asks']),budget//3)
            sim.resolve_asks(out['asks'])
        sim=compatible_sim(); ident=next(iter(sim.members))
        ask={'member_id':ident,'field':'constraints'}
        sim.resolve_asks([ask]); sim.resolve_asks([ask]) # legal across batches
        with self.assertRaises(ValueError): sim.resolve_asks([ask,ask])
        # Answered and declined asks are legal (though greedy avoids them).
        sim=compatible_sim(); m=next(iter(sim.members.values())); set_field(m,'schedule',None,'declined')
        sim.resolve_asks([{'member_id':m['member_id'],'field':'constraints'}])
        self.assertIsNone(m['fields']['schedule'])

    def test_guard_rejects_bad_candidates_using_official_validator(self):
        for budget in range(13):
            sim=compatible_sim(8,unknown=True); sim.ask_spent=12-budget
            ids=list(sim.members); sim.busy[ids[-1]]=8
            candidates=[{'member_id':i,'field':f} for i in ids+['nonexistent'] for f in ['constraints']+SOFT+['invalid']]
            candidates += candidates[:8]
            out=sanitize(sim.observe(),'ask',candidates)
            self.assert_action(sim.observe(),'ask',out); sim.resolve_asks(out['asks'])
        sim=compatible_sim(6); ids=list(sim.members); state=sim.observe()
        candidates=[[ids[0],ids[1]],[ids[1],ids[0]],[ids[0],ids[2]],[ids[3],ids[4]],[ids[5],ids[5]],['missing',ids[5]]]
        out=sanitize(state,'match',candidates)
        self.assert_action(state,'match',out); sim.advance(out['pairs'])
        self.assert_action(sim.observe(),'match',decide(request(sim.observe())))
        for _ in range(40): sim.advance([])
        state=sim.observe()
        out=sanitize(state,'match',candidates)
        self.assert_action(state,'match',out); sim.advance(out['pairs'])

    def test_seeded_properties_and_official_episode_transitions(self):
        # 18 episodes, 2160 decisions; public stress seeds, never selection seeds.
        for variant in VARIANTS:
            for seed in (24011,24012,24013):
                sim=Simulator(generate(seed,40,'hardening',variant)); memory=None
                for day in range(60):
                    for phase in ('ask','match'):
                        state=sim.observe(); req=request(state,phase,memory); saved=copy.deepcopy(req)
                        out=decide(req)
                        self.assertEqual(req,saved)
                        self.assertEqual(out,decide(request(state,phase,{'stale':'ignored'})))
                        self.assertEqual(out['asks' if phase=='ask' else 'pairs'], (baseline_asks if phase=='ask' else baseline_match)(state))
                        self.assert_action(state,phase,out); memory=out['memory']
                        self.assertTrue(all(m['arrived_day']<=day for m in state['members']))
                        self.assertTrue(all(e['observed_day']<=day for e in state['feedback']))
                        self.assertFalse(any(k in m for m in state['members'] for k in ('truth','bias','response_rate','exit_day')))
                        (sim.resolve_asks if phase=='ask' else sim.advance)(out['asks' if phase=='ask' else 'pairs'])
                for _ in range(40): sim.advance([]) # official runner does not invoke policy here

    def test_hidden_world_changes_cannot_change_observation_decision(self):
        sim=compatible_sim(8); other=copy.deepcopy(sim)
        for m in other.members.values():
            m['bias']=-100; m['response_rate']=0; m['second_bias']=100
            m['truth']['relationship_goal']='exploring'
        future=generate(24021,1)['members'][0]; future['arrived_day']=20
        other.members[future['member_id']]=future
        self.assertEqual(sim.observe(),other.observe())
        for phase in ('ask','match'):
            self.assertEqual(decide(request(sim.observe(),phase)),decide(request(other.observe(),phase)))

    def test_high_predictions_never_override_eligibility(self):
        from raven.config import config
        from raven.graphs import build
        for blocker in (None, ['other']):
            state=compatible_sim().observe(); set_field(state['members'][0],'acceptable_zones',blocker)
            with patch('raven.graphs.predict',return_value=1e100):
                self.assertEqual(build(state,config('joint'))[0],[])

    def test_public_feedback_lifecycle_fixtures(self):
        # Construct coherent public timelines using an actual generated introduction.
        cases=[('pending',None,None,None),('one_yes','yes',None,None),
               ('both_yes','yes','yes',None),('both_no','no','no',None),
               ('missing','yes',None,False),('late_date','yes','yes',True),
               ('second_pending','yes','yes',True),('pause','yes','yes',True)]
        for name,ra,rb,dated in cases:
            sim=compatible_sim(4); a,b=list(sim.members)[:2]
            sim.advance([[a,b]]); ident=sim.introductions[0]['introduction_id']; sim.events=[]
            def event(member,kind,value,day):
                return dict(introduction_id=ident,member_id=member,event=kind,value=value,
                            occurred_day=day if value is not None else None,observed_day=day)
            if name!='pending':
                sim.events.append(event(a,'introduction_response',ra,1))
                if name!='one_yes':sim.events.append(event(b,'introduction_response',rb,7 if rb is None else 2))
            if dated is True:
                day=35 if name=='late_date' else 8
                sim.events.append(event(None,'date_happened',True,day))
                sim.busy.update({a:day+6,b:day+6})
                if name=='pause':
                    sim.events.extend([event(a,'second_meeting_intention','yes',9),event(b,'second_meeting_intention','yes',10),
                                       event(None,'pause_after_mutual_interest',True,10)])
            for day in (1,2,7,8,10,14,35,41,59):
                sim.day=day;state=sim.observe()
                self.assertTrue(all(e['observed_day']<=day for e in state['feedback']))
                for phase in ('ask','match'):
                    self.assert_action(state,phase,decide(request(state,phase)))
                self.assertNotIn(frozenset((a,b)),[frozenset(p) for p in decide(request(state))['pairs']])
                if name=='pause' and day>=10:
                    self.assertFalse(next(m for m in state['members'] if m['member_id']==a)['available'])
