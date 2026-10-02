from __future__ import annotations
import argparse,csv,json
from collections import defaultdict
from pathlib import Path

def load_mapping(path="config/job-family-mapping.json"):
    return json.loads(Path(path).read_text())

def apply(rows, config):
    known=config["mappings"]; out=[]; unknown=set()
    for row in rows:
        title=(row.get("duty_title") or "").strip()
        family=known.get(title)
        if family is None:
            family="unmapped/review"; unknown.add(title or "__MISSING__")
        item=dict(row); item["job_family"]=family; out.append(item)
    return out,sorted(unknown)

def coverage(rows):
    out=defaultdict(lambda:{"rows":0,"certificated_fte":0.0,"classified_fte":0.0})
    for r in rows:
        x=out[(r["school_year"],r["job_family"])]
        x["rows"]+=1; x["certificated_fte"]+=float(r.get("certificated_fte") or 0); x["classified_fte"]+=float(r.get("classified_fte") or 0)
    return [{"school_year":y,"job_family":f,**v,"total_fte":v["certificated_fte"]+v["classified_fte"]} for (y,f),v in sorted(out.items())]

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("--input",default="artifacts/normalized/rsd407.csv"); ap.add_argument("--mapping",default="config/job-family-mapping.json"); ap.add_argument("--output",default="artifacts/normalized/rsd407-job-family.csv"); ap.add_argument("--coverage",default="artifacts/normalized/job-family-coverage.json")
    a=ap.parse_args(); cfg=load_mapping(a.mapping)
    with Path(a.input).open(newline="",encoding="utf-8") as h: rows=list(csv.DictReader(h))
    enriched,unknown=apply(rows,cfg)
    if unknown: raise RuntimeError("unmapped OSPI Duty Title values: "+", ".join(unknown))
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="",encoding="utf-8") as h:
        w=csv.DictWriter(h,fieldnames=list(enriched[0])+["job_family"]); w.writeheader(); w.writerows(enriched)
    Path(a.coverage).write_text(json.dumps({"schema_version":1,"source":a.input,"rows":coverage(enriched)},indent=2)+"\n")
    print(f"mapped {len(enriched)} employee-year rows with zero unknown duty titles")
if __name__=="__main__": main()
