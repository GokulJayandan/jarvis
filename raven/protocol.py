"""One-request process boundary; diagnostics are stderr only."""
import json
import os
import sys
import traceback
from .config import config
from .clarification import questions
from .graphs import build
from .matching import allocate
from .validation import sanitize

def decide(request,name='final'):
    phase=request.get('phase')
    if phase not in ('ask','match'): raise ValueError('Unsupported phase')
    state=request.get('state',{})
    if not state.get('members'): return {'asks' if phase=='ask' else 'pairs':[],'memory':{}}
    cfg=config(name)
    if 'official_baseline' in cfg:
        from official_policy import decide as baseline
        response=baseline(request,cfg['official_baseline'])
        return sanitize(state,phase,response['asks' if phase=='ask' else 'pairs'])
    # Deterministic bounded work on unusually large, otherwise valid observations.
    # Omitted members remain unserved for this invocation; no unknown edge is used.
    if len(state.get('members',[]))>220:
        state=dict(state,members=sorted(state['members'],key=lambda m:m['member_id'])[:220])
    if phase=='ask' and cfg.get('ask_backend')=='official':
        from kit import baseline_asks
        action=baseline_asks(state)
    elif phase=='match' and cfg.get('match_backend')=='official':
        from kit import baseline_match
        action=baseline_match(state)
    else:
        action=questions(state,cfg) if phase=='ask' else allocate(build(state,cfg,False)[0],cfg['matcher'])
    return sanitize(state,phase,action)

def main(name='final'):
    request={}
    try:
        raw=sys.stdin.buffer.read(1024*1024+1)
        if len(raw)>1024*1024: raise ValueError('Request exceeds 1 MiB')
        request=json.loads(raw,parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
        response=decide(request,name)
    except Exception:
        traceback.print_exc(limit=4,file=sys.stderr)
        if os.environ.get('RAVEN_STRICT')=='1':
            raise
        phase=request.get('phase') if isinstance(request,dict) else None
        response={'asks' if phase=='ask' else 'pairs':[],'memory':{}}
    sys.stdout.write(json.dumps(response,allow_nan=False,separators=(',',':'))+'\n')
