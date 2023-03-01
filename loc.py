"""
Q&D script to get a rough estimate of total KBase lines of code.

Super inefficient. Better to just use this in the future:
https://github.com/boyter/scc
"""

from collections import defaultdict
import requests
import sys
import time


_LANGS = {"Java", "Python", "Go", "JavaScript", "Perl", "C", "C Header", "C++", "PHP", "R",
          "Ruby", "TypeScript"}
_URL = "https://api.codetabs.com/v1/loc/?github="
_REQ_LIMIT_SEC = 6  # https://codetabs.com/count-loc/count-loc-online.html  +1 for fudge factor
_RETRY_DELAY = [6, 12, 18, 24]


def get_response(repo):
    exp = None
    for t in _RETRY_DELAY:
        try:
            res = requests.get(_URL + repo)
            if not res.ok:
                print(res.text, file=sys.stderr)
                res.raise_for_status()
            return res
        except Exception as e:
            exp = e
            print(f"Retrying in {t} sec: {str(e)}", file=sys.stderr)
            time.sleep(t)
    raise exp


def main():
    with open(sys.argv[1]) as repofile:
        repos = []
        for r in repofile:
            r = r.strip()
            if r and r[0] != '#':
                repos.append(r)
    repos = sorted(set(repos))  # remove duplicates
    print(f"Repo count: {len(repos)}, estimated execution time "
        + f"{len(repos) * (_REQ_LIMIT_SEC)} sec")
    totals = defaultdict(int)
    ignored = set()
    for r in repos:
        print(r)
        t = time.time()  # TODO move this into get_response and return the last request time
        res = get_response(r)
        res = {r["language"]: r for r in res.json()}
        ignored.update({l for l in res if l not in _LANGS})
        res = {l: res[l] for l in _LANGS if l in res}
        totalcount = 0
        for l in sorted(res):
            count = res[l]["linesOfCode"] + res[l]["comments"]
            totalcount += count
            totals[l] += count
            print(f"\t{l}: {count}")
        print(f"\tTotal: {totalcount}")
        wait = _REQ_LIMIT_SEC - time.time() + t
        if wait > 0:
            time.sleep(wait)
    print("Totals:")
    totalcount = 0
    for l in sorted(totals):
        totalcount += totals[l]
        print(f"\t{l}: {totals[l]}")
    print(f"\tTotal: {totalcount}")
    print(f"Ignored fields: {', '.join(sorted(ignored))}")


if __name__ == "__main__":
    main()

