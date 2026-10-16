"""Direct experiment adapter, independent of the official baseline entrypoint."""
import argparse
from raven.protocol import main

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--baseline',default='greedy')
    parser.add_argument('--config',default='final')
    args=parser.parse_args()
    main(args.config)
