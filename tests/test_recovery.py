import unittest
from unittest.mock import patch
from kit import Simulator, generate, baseline_asks, baseline_match
from raven.config import config
from raven.protocol import decide
from raven.validation import sanitize

class Recovery(unittest.TestCase):
    def test_hybrid_components(self):
        sim=Simulator(generate(23001,40))
        for phase,backend,fn in [('ask','ask_backend',baseline_asks),('match','match_backend',baseline_match)]:
            state=sim.observe()
            with patch('raven.protocol.config',return_value=dict(config('joint'),**{backend:'official'})):
                self.assertEqual(decide({'phase':phase,'state':state}),sanitize(state,phase,fn(state)))

    def test_guarded_baseline_complete_episode(self):
        from official_policy import decide as official
        sim=Simulator(generate(23002,40))
        for day in range(60):
            for phase in ('ask','match'):
                request={'phase':phase,'state':sim.observe(),'memory':{}}
                with patch('raven.protocol.config',return_value={'official_baseline':'greedy'}):
                    response=decide(request)
                self.assertEqual(response,official(request))
                if phase=='ask':sim.resolve_asks(response['asks'])
                else:sim.advance(response['pairs'])
