"""Official deterministic disclosure semantics, never infer declined values."""
from .constraints import HARD

def disclosure_probability(member, field):
    keys=HARD if field=='constraints' else (field,)
    missing=[k for k in keys if member.get('fields',{}).get(k) is None]
    return float(all(member.get('field_status',{}).get(k)!='declined' for k in missing))
