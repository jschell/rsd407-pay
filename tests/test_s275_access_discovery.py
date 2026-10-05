from rsd407_pay.s275_access_discovery import run
def test_run_attempts_every_year(monkeypatch):
    import rsd407_pay.s275_access_discovery as m
    schema={"resources":[{"school_year":"2013-14","database_file":"a","schema":{"tables":["T"]}},
                         {"school_year":"2014-15","database_file":"b","schema":{"tables":["T"]}}]}
    def inspect(db,table,year):
        if year=="2013-14": raise RuntimeError("first problem")
        return {"status":"observed","school_year":year,"recno_1_comparison":{"row_difference":1,"fte_difference":2}}
    monkeypatch.setattr(m,"inspect_year",inspect)
    d=run(schema)
    assert d["summary"]["years_attempted"]==2
    assert d["summary"]["years_error"]==1
    assert d["years"][1]["school_year"]=="2014-15"
