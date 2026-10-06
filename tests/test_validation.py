import unittest
from rsd407_pay.validation import YEARS, validate

def metrics():
    years=[]
    for y in range(2013,2025):
        sy=f"{y}-{str(y+1)[-2:]}"
        years.append({"school_year":sy,"employee_rows":100,"total_fte":90,"base_salary":1_000_000,"total_salary":1_100_000,"reported_employer_compensation":1_300_000})
    return {"district":years}

def rows():
    out=[]
    for i,y in enumerate(range(2013,2025)):
        sy=f"{y}-{str(y+1)[-2:]}"
        out.append({"school_year":sy,"source_sha256":str(i),"source_sheet":"S","source_row":str(i+1),"certificated_fte":"1","classified_fte":"0","base_salary":"1","total_salary":"1","insurance_benefits":"0","mandatory_benefits":"0"})
    return out

class ValidationTests(unittest.TestCase):
    def test_valid_rows_pass(self):
        self.assertEqual(validate(rows(),metrics())["status"],"pass")
    def test_negative_pay_fails(self):
        r=rows(); r[0]["base_salary"]="-1"
        self.assertEqual(validate(r,metrics())["status"],"fail")
    def test_duplicate_source_row_fails(self):
        r=rows(); r.append(dict(r[0]))
        self.assertEqual(validate(r,metrics())["status"],"fail")

if __name__=="__main__": unittest.main()


class ExternalValidationTests(unittest.TestCase):
    def test_external_reconciliation_is_reported_and_gated(self):
        from rsd407_pay.validation import validate
        rows=[]
        for year in YEARS:
            rows.append({"school_year":year,"source_sha256":year,"source_sheet":"Sheet1","source_row":"1","certificated_fte":"1","classified_fte":"0","base_salary":"1","total_salary":"1","insurance_benefits":"0","mandatory_benefits":"0"})
        metrics={"district":[{"school_year":y,"employee_rows":1,"total_fte":1,"base_salary":1,"total_salary":1,"reported_employer_compensation":1} for y in YEARS]}
        ext={"status":"pass","control":"OSPI Personnel Summary Table 45B","years":[{"school_year":y,"status":"pass"} for y in YEARS[-6:]]}
        report=validate(rows,metrics,ext)
        assert report["status"]=="pass"
        assert report["external_reconciliation"]["checked_years"]==YEARS[-6:]
        assert report["external_reconciliation"]["unavailable_annual_report_years"]==YEARS[:6]
        ext["status"]="fail"
        assert validate(rows,metrics,ext)["status"]=="fail"
    