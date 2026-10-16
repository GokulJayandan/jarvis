"""Require identical episode actions and outcomes across local/container runs."""
import json
import sys

def compare(first,second):
    a=json.load(open(first));b=json.load(open(second))
    assert a['summary']['eligible'] and b['summary']['eligible'],'Invalid episode'
    left={(r['variant'],r['seed']):r for r in a['episodes']}
    right={(r['variant'],r['seed']):r for r in b['episodes']}
    assert set(left)==set(right),'Episode sets differ'
    for key in left:
        x={k:v for k,v in left[key].items() if k!='inference_seconds'}
        y={k:v for k,v in right[key].items() if k!='inference_seconds'}
        assert x==y,'Actions or outcomes differ for '+str(key)
    print(json.dumps({'same_actions_and_outcomes':True,'episodes':len(left)}))

if __name__=='__main__':compare(*sys.argv[1:])
