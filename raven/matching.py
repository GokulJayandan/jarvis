"""Integer-weight blossom solver with greedy safeguard for oversized observations."""
from .graphs import ConfirmedEdge

def greedy(edges):
    used=set(); pairs=[]
    for e in sorted(edges,key=lambda e:(-e.weight,e.a,e.b)):
        if e.weight>0 and e.a not in used and e.b not in used:
            pairs.append([e.a,e.b]);used.update((e.a,e.b))
    return sorted(pairs)

class Graph:
    """Minimal undirected graph API used by the vendored NetworkX blossom routine."""
    def __init__(self, edges):
        self.adj={}
        for e in sorted(edges,key=lambda e:(e.a,e.b)):
            if e.weight<=0: continue
            data={'weight':max(1,round(e.weight*1000000000))}
            previous=self.adj.get(e.a,{}).get(e.b)
            if previous is not None and previous['weight']>=data['weight']: continue
            self.adj.setdefault(e.a,{})[e.b]=data
            self.adj.setdefault(e.b,{})[e.a]=data
    def __iter__(self): return iter(self.adj)
    def __getitem__(self,node): return self.adj[node]
    def nodes(self): return self.adj.keys()
    def neighbors(self,node): return self.adj[node].keys()
    def edges(self,data=False):
        for a,neighbors in self.adj.items():
            for b,attrs in neighbors.items():
                if a<b: yield (a,b,attrs) if data else (a,b)

def allocate(edges, mode='exact'):
    if any(not isinstance(e,ConfirmedEdge) for e in edges):
        raise TypeError('Only confirmed edges may be allocated')
    if not edges: return []
    if mode=='greedy' or len(edges)>6000 or len({i for e in edges for i in (e.a,e.b)})>220: return greedy(edges)
    from .vendor.blossom import max_weight_matching
    return sorted(sorted(pair) for pair in max_weight_matching(Graph(edges)))
