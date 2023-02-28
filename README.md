## KBase LOC counter

Extremely nasty and inefficient means to get an estimate of the total lines of code in KBase.

### Usage

Install requests, then

```
python loc.py repos.txt
```

### TODO

* Add UI repos, currently missing LOC from there
* Try to pull prod released repos from the catalog vs. including them in `repos.txt`
  * Tricky as it's a mix of kbase and non-kbase code and some git URLs 404