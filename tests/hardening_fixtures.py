"""Public-schema fixtures. Private world data never crosses the policy boundary."""
import copy
import json
from kit import generate, Simulator, HARD, SOFT, OPTIONS, VERSION


def compatible_sim(n=2, seed=24001, unknown=False):
    world = generate(seed, n, 'hardening')
    fields = dict(age_min=18, age_max=65, who_to_meet=['woman', 'man', 'non_binary'],
                  relationship_structure='monogamous', smoking='no', partner_smoking='any',
                  has_children=False, partner_children='any', wants_children='unsure',
                  acceptable_zones=['zone_a'], schedule=['weekend_day'])
    fields.update({k: v[0] for k, v in OPTIONS.items()})
    for m in world['members']:
        m.update(arrived_day=0, exit_day=10000, zone='zone_a')
        m['truth'] = copy.deepcopy(fields)
        m['fields'] = {k: None if unknown else copy.deepcopy(v) for k, v in fields.items()}
        m['field_status'] = {k: 'not_asked' if unknown else 'observed' for k in fields}
        m['field_observed_day'] = {k: None if unknown else 0 for k in fields}
    return Simulator(world)


def set_field(member, field, value, status=None, day=0):
    member['fields'][field] = copy.deepcopy(value)
    member['field_status'][field] = status or ('not_asked' if value is None else 'observed')
    member['field_observed_day'][field] = None if value is None else day


def request(state, phase='match', memory=None):
    return dict(schema_version=VERSION, phase=phase, state=state, memory=memory)


def payload(req):
    return json.dumps(req, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode('utf-8')


def near_limit_request(phase='match', dense=False):
    # No official member-count cap: use the actual 1 MiB request cap.
    lo, hi = 0, 1400
    while lo + 1 < hi:
        n = (lo + hi) // 2
        req = request(compatible_sim(n, unknown=not dense).observe(), phase)
        if len(payload(req)) <= 1024**2 - 4096:
            lo = n
        else:
            hi = n
    req = request(compatible_sim(lo, unknown=not dense).observe(), phase)
    req['memory'] = ''
    req['memory'] = 'x' * (1024**2 - len(payload(req)))
    assert len(payload(req)) == 1024**2
    return req
