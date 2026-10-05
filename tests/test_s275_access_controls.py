import subprocess
from pathlib import Path
from rsd407_pay.s275_access_controls import derive

def test_personnel_rows_are_deduplicated_by_recno(monkeypatch):
    header="codist,recno,certfte,clasfte,certbase,clasbase,othersal,tfinsal,cins,cman,assfte"
    row1="17407,1,1,.2,100,20,5,140,10,15,.5"
    row2="17407,1,1,.2,100,20,5,140,10,15,.7"
    row3="17407,2,0,.8,0,80,2,90,8,9,.8"
    class R: stdout="\n".join([header,row1,row2,row3])
    monkeypatch.setattr(subprocess,"run",lambda *a,**k:R())
    d=derive(Path("x.accdb"),"T","2024-25")
    assert d["source_rows"]==3
    assert d["unique_personnel"]==2
    assert d["assignment_duplicate_rows"]==1
    assert d["total_fte"]==2.0
    assert d["base_salary"]==200.0
    assert d["tfinsal"]==230.0
    assert d["reported_employer_compensation"]==272.0

def test_personnel_field_disagreement_fails(monkeypatch):
    class R: stdout="codist,recno,certfte,clasfte,certbase,clasbase,othersal,tfinsal,cins,cman\n17407,1,1,0,100,0,0,100,1,1\n17407,1,.5,0,100,0,0,100,1,1"
    monkeypatch.setattr(subprocess,"run",lambda *a,**k:R())
    try: derive(Path("x"),"T","2024-25")
    except RuntimeError as e: assert "vary within recno" in str(e)
    else: assert False
