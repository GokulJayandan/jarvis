"""Team Jarvis submission adapter; official baselines preserved separately."""
import argparse
from raven.protocol import decide, main

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--baseline',choices=['greedy','no_asks','random'],default='greedy')
    args=parser.parse_args()
    if args.baseline=='greedy':
        main()
    else:
        import json,sys
        from official_policy import decide as official_decide
        print(json.dumps(official_decide(json.load(sys.stdin),args.baseline),allow_nan=False))
