"""Independent transcription of release 1.0 hard rules, differentially tested."""
from enum import Enum

HARD = ('age_min','age_max','who_to_meet','relationship_structure','smoking',
        'partner_smoking','has_children','partner_children','wants_children',
        'acceptable_zones','schedule')
SOFT = ('relationship_goal','relationship_pace','lifestyle','conversations',
        'emotional_availability','space_for_relationship','relocate')

class Status(str, Enum):
    CONFIRMED_FEASIBLE = 'feasible'
    CONFIRMED_INFEASIBLE = 'infeasible'
    UNKNOWN_PENDING_CLARIFICATION = 'needs_clarification'

def eligibility(a, b):
    if a['member_id'] == b['member_id'] or a['pool_id'] != b['pool_id'] or min(a['age'],b['age']) < 18:
        return Status.CONFIRMED_INFEASIBLE
    fa, fb = a.get('fields', {}), b.get('fields', {})
    for x,y,f,g in ((a,b,fa,fb),(b,a,fb,fa)):
        if f.get('age_min') is not None and y['age'] < f['age_min']: return Status.CONFIRMED_INFEASIBLE
        if f.get('age_max') is not None and y['age'] > f['age_max']: return Status.CONFIRMED_INFEASIBLE
        if f.get('who_to_meet') is not None and y['gender'] not in f['who_to_meet']: return Status.CONFIRMED_INFEASIBLE
        if f.get('acceptable_zones') is not None and y['zone'] not in f['acceptable_zones']: return Status.CONFIRMED_INFEASIBLE
        if f.get('partner_smoking') == 'no_smoking' and g.get('smoking') in ('yes','occasionally'): return Status.CONFIRMED_INFEASIBLE
        if f.get('partner_children') == 'no_children' and g.get('has_children') is True: return Status.CONFIRMED_INFEASIBLE
    if fa.get('relationship_structure') is not None and fb.get('relationship_structure') is not None and fa['relationship_structure'] != fb['relationship_structure']: return Status.CONFIRMED_INFEASIBLE
    if {fa.get('wants_children'), fb.get('wants_children')} == {'yes','no'}: return Status.CONFIRMED_INFEASIBLE
    if fa.get('schedule') is not None and fb.get('schedule') is not None and not set(fa['schedule']).intersection(fb['schedule']): return Status.CONFIRMED_INFEASIBLE
    if any(f.get(k) is None for f in (fa,fb) for k in HARD): return Status.UNKNOWN_PENDING_CLARIFICATION
    return Status.CONFIRMED_FEASIBLE

def missing_hard(member):
    return tuple(k for k in HARD if member.get('fields', {}).get(k) is None)

def recoverable(member):
    return not any(member.get('field_status', {}).get(k) == 'declined' for k in missing_hard(member))
