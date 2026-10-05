import subprocess
from pathlib import Path
from rsd407_pay.s275_access_inventory import schema

def test_schema_uses_whole_database_export(monkeypatch):
    calls=[]
    class R:
        def __init__(self,stdout): self.stdout=stdout
    def run(args,**kwargs):
        calls.append(args)
        if args[0]=="mdb-tables": return R("Personnel\nAssignments\n")
        if args[0]=="mdb-schema": return R("CREATE TABLE [Personnel] (...);\n")
        raise AssertionError(args)
    monkeypatch.setattr(subprocess,"run",run)
    result=schema(Path("sample.accdb"))
    assert result["tables"]==["Personnel","Assignments"]
    assert "CREATE TABLE" in result["schema_sql"]
    assert calls==[
        ["mdb-tables","-1","sample.accdb"],
        ["mdb-schema","sample.accdb"],
    ]
