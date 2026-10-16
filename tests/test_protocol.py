import copy
import json
import subprocess
import sys
import unittest
from evaluate import invoke,validate_response
from kit import Simulator,generate
from raven.validation import sanitize
from raven.protocol import decide
from tests.test_constraints import pair

class Protocol(unittest.TestCase):
    def test_empty(self):
        for phase in ('ask','match'):
            request={'phase':phase,'state':{'members':[]},'memory':None}
            response,elapsed=invoke([sys.executable,'raven_policy.py'],request)
            self.assertEqual(response,{'asks' if phase=='ask' else 'pairs':[],'memory':{}})
            self.assertLess(elapsed,10)
    def test_malformed(self):
        for raw in ('invalid','[]','{"phase":"wrong"}','{"memory":NaN}'):
            p=subprocess.run([sys.executable,'raven_policy.py'],input=raw,text=True,capture_output=True)
            self.assertEqual(p.returncode,0);json.loads(p.stdout)
            self.assertTrue(p.stderr)
    def test_large_memory_reset(self):
        for memory in (None,{}, {'previous_episode':'x'*500000}):
            self.assertEqual(decide({'phase':'match','state':{'members':[]},'memory':memory}),{'pairs':[],'memory':{}})
    def test_sanitizer(self):
        a,b=pair();state={'members':[a,b],'ask_budget_remaining':3,'introductions':[]}
        asks=[{'member_id':a['member_id'],'field':'constraints'}]*3+[{'member_id':'missing','field':'constraints'}]
        self.assertEqual(len(sanitize(state,'ask',asks)['asks']),1)
        pairs=[[a['member_id'],b['member_id']]]*2
        self.assertEqual(len(sanitize(state,'match',pairs)['pairs']),1)
        state['introductions']=[{'user_a':a['member_id'],'user_b':b['member_id']}]
        self.assertEqual(sanitize(state,'match',pairs)['pairs'],[])
    def test_unavailable_and_unknown(self):
        a,b=pair();a['available']=False;state={'members':[a,b]}
        self.assertEqual(sanitize(state,'match',[[a['member_id'],b['member_id']]])['pairs'],[])
        a['available']=True;a['fields']['schedule']=None
        self.assertEqual(sanitize(state,'match',[[a['member_id'],b['member_id']]])['pairs'],[])
