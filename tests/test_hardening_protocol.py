"""Actual stdout bytes, fresh processes, failure injection and payload boundaries."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from evaluate import LIMIT, validate_response, strict_json
from tests.hardening_fixtures import compatible_sim, request, payload, near_limit_request

ROOT=Path(__file__).resolve().parents[1]


class HardeningProtocol(unittest.TestCase):
    def invoke(self, req, command=None, minimal_env=False):
        env={k:v for k,v in os.environ.items() if k in ('SystemRoot','WINDIR','TEMP','TMP')} if minimal_env else dict(os.environ)
        env.pop('RAVEN_STRICT',None); env['PYTHONDONTWRITEBYTECODE']='1'
        with tempfile.TemporaryDirectory() as cwd:
            p=subprocess.run(command or [sys.executable,str(ROOT/'policy.py')], input=payload(req),
                             capture_output=True,cwd=cwd,env=env,timeout=10)
            self.assertEqual(list(Path(cwd).iterdir()),[])
        self.assertEqual(p.returncode,0,p.stderr[:2000])
        self.assertLessEqual(len(p.stdout),LIMIT); self.assertLessEqual(len(p.stderr),LIMIT)
        self.assertEqual(p.stdout.count(b'\n'),1)
        self.assertTrue(p.stdout.endswith(b'\n'))
        out=strict_json(p.stdout.decode('utf-8')) # rejects extra object/diagnostics
        validate_response(out,req['phase'])
        self.assertLessEqual(len(json.dumps(out['memory']).encode()),LIMIT)
        return out,p

    def test_empty_single_pair_and_optional_feedback(self):
        for n in (0,1,2,8):
            for phase in ('ask','match'):
                req=request(compatible_sim(n).observe(),phase)
                out,p=self.invoke(req,minimal_env=True)
                self.assertEqual(p.stderr,b''); self.assertEqual(out['memory'],{})

    def test_near_max_memory_and_foreign_schemas_ignored(self):
        req=request(compatible_sim(2).observe())
        expected,_=self.invoke(req)
        for memory in (None,{},[],42,False,'old',{'version':-1,'candidate':['missing','bad']},'x'*(LIMIT-4096)):
            req['memory']=memory
            out,p=self.invoke(req)
            self.assertEqual(out,expected); self.assertEqual(p.stderr,b'')

    def test_exact_input_byte_limit_dense_and_unknown(self):
        for dense in (False,True):
            for phase in ('ask','match'):
                req=near_limit_request(phase,dense)
                self.assertEqual(len(payload(req)),LIMIT)
                out,p=self.invoke(req)
                self.assertEqual(p.stderr,b'')
                if phase=='match':
                    self.assertEqual(len(out['pairs']),len(req['state']['members'])//2 if dense else 0)

    def test_memory_roundtrips_independent_processes(self):
        state=compatible_sim(4).observe(); memory=None
        for _ in range(6):
            for phase in ('ask','match'):
                out,p=self.invoke(request(state,phase,memory))
                self.assertEqual(p.stderr,b''); memory=json.loads(json.dumps(out['memory']))
        self.assertEqual(self.invoke(request(state))[0],self.invoke(request(state,memory=memory))[0])

    def test_python_hash_seed_does_not_change_actions(self):
        req=request(compatible_sim(20).observe())
        results=[]
        for seed in ('0','1','4294967295'):
            from unittest.mock import patch
            with patch.dict(os.environ,{'PYTHONHASHSEED':seed}): results.append(self.invoke(req)[0])
        self.assertTrue(all(x==results[0] for x in results))

    def test_long_real_feedback_history(self):
        from kit import Simulator,generate,baseline_asks,baseline_match
        sim=Simulator(generate(24061,200,'hardening','delayed'))
        for _ in range(60):
            sim.resolve_asks(baseline_asks(sim.observe()))
            sim.advance(baseline_match(sim.observe()))
        for _ in range(40):sim.advance([])
        state=sim.observe()
        self.assertGreater(len(state['feedback']),100)
        self.assertTrue(any(e['member_id'] is None for e in state['feedback']))
        for phase in ('ask','match'):
            # Follow-up calls aren't made by the harness; this is a contract-state probe.
            out,p=self.invoke(request(state,phase)); self.assertEqual(p.stderr,b'')

    def test_research_failures_yield_legal_empty_fallback(self):
        from kit import Simulator
        for phase,target in (('ask','raven.clarification.exhaustive'),('match','raven.vendor.blossom.max_weight_matching')):
            for error in ('RuntimeError','TimeoutError','MemoryError'):
                sim=compatible_sim(4,unknown=phase=='ask')
                code=(f"import sys;sys.path.insert(0,{str(ROOT)!r});"
                      "from unittest.mock import patch;from raven.protocol import main;"
                      f"p=patch('{target}',side_effect={error}('injected'));p.start();main('joint')")
                out,p=self.invoke(request(sim.observe(),phase),[sys.executable,'-c',code])
                self.assertTrue(p.stderr)
                action=out['asks' if phase=='ask' else 'pairs']
                self.assertEqual(action,[])
                (sim.resolve_asks if phase=='ask' else sim.advance)(action)

    def test_defensive_malformed_not_contract_requirements(self):
        for raw in (b'',b'no json',b'[]',b'null',b'{"phase":"ask","memory":NaN}',
                    b'{"phase":"match","memory":Infinity}',b'{"phase":"wrong"}',b'\xff',b' '* (LIMIT+1)):
            env=dict(os.environ); env.pop('RAVEN_STRICT',None)
            p=subprocess.run([sys.executable,str(ROOT/'policy.py')],input=raw,capture_output=True,env=env,timeout=10)
            self.assertEqual(p.returncode,0)
            out=strict_json(p.stdout.decode('utf-8'))
            self.assertEqual(out['memory'],{}); self.assertTrue(p.stderr)
            self.assertLess(len(p.stderr),LIMIT)
