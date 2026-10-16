"""Endpoint screening preserves whole high-value complementary groups when possible."""
def screen(candidates, potential, limit, future=None):
    scores={q:(future or {}).get(q,0) for q in candidates}
    for edge in potential:
        for q in edge.requirements:
            if q in scores: scores[q]+=edge.weight/len(edge.requirements)
    ranked=sorted(candidates,key=lambda q:(-scores[q],q))
    kept=[]
    # Half the slots favor the best complete requirement groups.
    for edge in sorted(potential,key=lambda e:(-e.weight,e.a,e.b)):
        additions=sorted(edge.requirements-set(kept))
        if len(kept)+len(additions)<=max(2,limit//2): kept.extend(additions)
    for q in ranked:
        if q not in kept and len(kept)<limit: kept.append(q)
    return sorted(kept[:limit])
