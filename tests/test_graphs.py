import unittest
from unittest.mock import patch
from raven.config import config
from raven.graphs import build
from raven.clarification import questions
from raven.constraints import HARD
from tests.test_constraints import pair

class Graphs(unittest.TestCase):
    def state(self):
        a,b=pair();return {'members':[a,b],'introductions':[],'day':0,'ask_budget_remaining':12}
    @patch('raven.graphs.predict',return_value=.1)
    @patch('raven.graphs.feasibility_probability',return_value=.5)
    def test_graph_separation(self,*mocks):
        state=self.state();confirmed,potential=build(state,config('joint'))
        self.assertEqual((len(confirmed),len(potential)),(1,0))
        state['members'][0]['fields']['schedule']=None
        confirmed,potential=build(state,config('joint'))
        self.assertEqual((len(confirmed),len(potential)),(0,1))
        self.assertEqual(len(potential[0].requirements),1)
        state['members'][1]['fields']['age_min']=None
        self.assertEqual(len(build(state,config('joint'))[1][0].requirements),2)
    @patch('raven.graphs.predict',return_value=.1)
    @patch('raven.graphs.feasibility_probability',return_value=.5)
    def test_past_pairs_excluded(self,*mocks):
        state=self.state();a,b=state['members'];state['introductions']=[{'user_a':a['member_id'],'user_b':b['member_id']}]
        self.assertEqual(build(state,config('joint')),([],[]))
    def test_zero_budget(self):
        state=self.state();state['ask_budget_remaining']=0
        self.assertEqual(questions(state,config('joint')),[])
    @patch('raven.clarification.future_value',return_value=0)
    @patch('raven.graphs.predict',return_value=.1)
    @patch('raven.graphs.feasibility_probability',return_value=.5)
    def test_joint_vs_singleton(self,*mocks):
        state=self.state()
        for m in state['members']:m['fields']['schedule']=None
        self.assertEqual(len(questions(state,config('joint'))),2)
        self.assertEqual(questions(state,config('singleton')),[])
    def test_no_repeat_disclosed_asks(self):
        self.assertEqual(questions(self.state(),config('joint')),[])
