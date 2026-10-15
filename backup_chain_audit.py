"""Offline, bounded captured-input analysis. Original implementation, MIT."""
import argparse
import json
import re
import sys
from pathlib import Path

class InputError(ValueError):
    pass

def obj(x,required,optional=()):
    if not isinstance(x,dict) or set(x)-set(required)-set(optional) or set(required)-set(x):
        raise InputError("object keys do not match the documented contract")
    return x

def arr(x,limit=512):
    if not isinstance(x,list) or len(x)>limit:raise InputError("expected a bounded array")
    return x

def text(x):
    if not isinstance(x,str) or not 1<=len(x)<=256:raise InputError("expected a nonempty string <=256 characters")
    return x

def integer(x,maximum=9223372036854775807):
    if type(x) is not int or not 0<=x<=maximum:raise InputError("expected bounded nonnegative integer")
    return x

def unique(xs):
    if len(set(xs))!=len(xs):raise InputError("duplicate identity")
    return xs

def pairs(ps):
    d={}
    for k,v in ps:
        if k in d:raise InputError("duplicate JSON key")
        d[k]=v
    return d

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("snapshot",type=Path);a=p.parse_args()
    try:
        with a.snapshot.open("rb") as f:raw=f.read(2*1024*1024+1)
        if len(raw)>2*1024*1024:raise InputError("snapshot exceeds2 MiB")
        d=json.loads(raw.decode("utf-8"),object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(InputError("nonfinite JSON")))
        result=analyze(d);print(json.dumps(result,sort_keys=True,ensure_ascii=True));return 1 if result.get("findings") else 0
    except (InputError,ValueError,TypeError,KeyError,OSError,RecursionError) as e:
        print(json.dumps({"error":str(e)}),file=sys.stderr);return 2

def analyze(d):
    obj(d,["snapshots","retain","delete"])
    nodes={}
    for s in arr(d["snapshots"]):
        obj(s,["id","parent","verified","bytes"])
        sid=text(s["id"])
        if sid in nodes:raise InputError("duplicate snapshot id")
        if s["parent"] is not None:text(s["parent"])
        if type(s["verified"]) is not bool:raise InputError("verified must be boolean")
        integer(s["bytes"]);nodes[sid]=s
    retain=unique([text(x) for x in arr(d["retain"])]);delete=unique([text(x) for x in arr(d["delete"])])
    if any(x not in nodes for x in delete):raise InputError("delete proposal names an unknown snapshot")
    findings=[];needed=set();chains=[]
    for root in retain:
        path=[];seen=set();cur=root;reason=None
        while cur is not None:
            if cur in seen:reason={"kind":"cycle","at":cur};break
            if cur not in nodes:reason={"kind":"missing_snapshot","at":cur};break
            seen.add(cur);path.append(cur)
            if not nodes[cur]["verified"]:reason={"kind":"unverified_snapshot","at":cur};break
            cur=nodes[cur]["parent"]
        if reason:findings.append({"retain":root,**reason})
        else:needed.update(path)
        chains.append({"retain":root,"restorable_from_declared_metadata":reason is None,"base_to_target":list(reversed(path)) if reason is None else [],"observed_target_to_base":path})
    blocked=sorted(set(delete)&needed)
    if blocked:findings.append({"kind":"retained_dependency_in_delete_proposal","snapshots":blocked})
    unknown_restore=any(not x["restorable_from_declared_metadata"] for x in chains)
    eligible=[] if unknown_restore else sorted(set(delete)-needed)
    return {"chains":chains,"needed_snapshots":sorted(needed),"needed_bytes":sum(nodes[x]["bytes"] for x in needed),"blocked_delete":blocked,"eligible_delete":eligible,"deletion_eligibility_withheld":unknown_restore,"findings":findings}

if __name__ == "__main__":
    raise SystemExit(main())
