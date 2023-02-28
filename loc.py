"""
Q&D script to get a rough estimate of total KBase lines of code.

Super inefficient. Better to just use this in the future:
https://github.com/boyter/scc
"""

from collections import defaultdict
import requests
import sys
import time


_LANGS = ["Java", "Python", "Go", "JavaScript", "Perl"]
_URL = "https://api.codetabs.com/v1/loc/?github="
_REQ_LIMIT_SEC = 5  # https://codetabs.com/count-loc/count-loc-online.html  


def main():
    langs = sorted(_LANGS)
    set_langs = set(langs)
    with open(sys.argv[1]) as repofile:
        repos = []
        for r in repofile:
            r = r.strip()
            if r and r[0] != '#':
                repos.append(r)
    repos = sorted(set(repos))  # remove duplicates
    print(f"Repo count: {len(repos)}, estimated execution time "
        + f"{len(repos) * (_REQ_LIMIT_SEC + 1)} sec")
    totals = defaultdict(int)
    ignored = set()
    for r in repos:
        print(r)
        t = time.time()
        res = requests.get(_URL + r)
        if not res.ok:
            print(res.text)
            res.raise_for_status()
        res = {r["language"]: r for r in res.json()}
        ignored.update({l for l in res if l not in set_langs})
        res = {l: res[l] for l in langs if l in res}
        totalcount = 0
        for l in res:
            count = res[l]["linesOfCode"] + res[l]["comments"]
            totalcount += count
            totals[l] += count
            print(f"\t{l}: {count}")
        print(f"\tTotal: {totalcount}")
        wait = _REQ_LIMIT_SEC - time.time() + t + 1  # engineering fudge factor
        if wait > 0:
            time.sleep(wait)
    print("Totals:")
    totalcount = 0
    for l in totals:
        totalcount += totals[l]
        print(f"\t{l}: {totals[l]}")
    print(f"\tTotal: {totalcount}")
    print(f"Ignored items: {','.join(sorted(ignored))}")


if __name__ == "__main__":
    main()

