from rsd407_pay.s275_access_sources import inventory

def test_discovers_all_final_access_years():
    links=[]
    for y in range(2013,2025):
        short=str(y+1)[-2:]
        links.append(f'<a href="/files/{y}.zip">{y}-{short} Final S-275 Personnel Database</a>')
    report=inventory("<html>"+"".join(links)+"</html>")
    assert report["status"]=="pass"
    assert report["missing_years"]==[]
    assert len(report["resources"])==12
    assert report["resources"][0]["school_year"]=="2013-14"
    assert report["resources"][-1]["school_year"]=="2024-25"

def test_does_not_accept_preliminary_or_simplified_files():
    html='<a href="/prelim.zip">2024-25 Preliminary S-275 Personnel Database</a><a href="/final.xlsx">2024-25 Final S-275 Personnel Excel</a>'
    report=inventory(html)
    assert report["resources"]==[]
    assert "2024-25" in report["missing_years"]
