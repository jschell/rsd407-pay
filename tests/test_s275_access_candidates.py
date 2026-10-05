import subprocess
from pathlib import Path
from rsd407_pay.s275_access_candidates import fields

def test_fields_reads_mdb_export_header(monkeypatch):
    class R:
        stdout='"DistrictCode","TotalFTE","BaseSalary"\n"17407","337.36","100000"\n'
    def run(args,**kwargs):
        assert args==["mdb-export","sample.accdb","Personnel"]
        return R()
    monkeypatch.setattr(subprocess,"run",run)
    assert fields(Path("sample.accdb"),"Personnel")==["DistrictCode","TotalFTE","BaseSalary"]
