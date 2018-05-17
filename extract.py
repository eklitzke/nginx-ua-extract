#!/usr/bin/env python

import argparse
import collections
import operator
import os
import re

UA_RE = re.compile(r'"(Mozilla[^"]*?)"')


def extract_log(file_obj, counts):
    for line in file_obj:
        m = UA_RE.search(line)
        if not m:
            continue
        counts[m.groups()[0]] += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', default='.')
    parser.add_argument('-c', '--count', default=10)
    args = parser.parse_args()

    counts = collections.defaultdict(int)
    for fname in os.listdir(args.directory):
        if fname.startswith('access.log'):
            with open(fname) as file_obj:
                extract_log(file_obj, counts)

    agents = list(
        sorted(counts.items(), key=operator.itemgetter(1), reverse=True))

    for agent, count in agents[:args.count]:
        print('{:<7d} {}'.format(count, agent))


if __name__ == '__main__':
    main()
