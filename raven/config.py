"""Configuration-driven research variants; inference defaults are frozen separately."""
import json
from pathlib import Path

DEFAULT = dict(planner='joint', candidate_limit=12, future_weight=0.0,
               predictor='logistic', calibration=True, matcher='exact',
               soft_questions=False, waiting_weight=0.0, portfolio_limit=1000)

def config(name='final'):
    out = DEFAULT.copy()
    if name == 'final':
        path = Path(__file__).parent / 'assets' / 'final_config.json'
        if path.exists():
            out.update(json.loads(path.read_text()))
    changes = {
        'random_questions': dict(planner='random'),
        'endpoint': dict(planner='endpoint'),
        'singleton': dict(planner='singleton'),
        'joint': {},
        'future': dict(future_weight=0.5),
        'future_high': dict(future_weight=2.0),
        'unpruned': dict(candidate_limit=10000, portfolio_limit=2000),
        'prior': dict(predictor='prior'),
        'uncalibrated': dict(calibration=False),
        'greedy_match': dict(matcher='greedy'),
        'soft': dict(soft_questions=True),
        'waiting': dict(waiting_weight=0.001),
    }
    if name != 'final':
        if name not in changes:
            raise ValueError('Unknown configuration: ' + name)
        out.update(changes[name])
    return out
