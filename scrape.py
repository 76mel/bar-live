import json, subprocess, tempfile, datetime, requests

CHARTS = {"wind": "windreport.gif", "sea": "seareport.gif", "atmos": "atmosreport.gif"}
H = {"Referer": "https://www.chimet.co.uk/", "User-Agent": "Mozilla/5.0"}
out = {"fetched": datetime.datetime.utcnow().isoformat() + "Z"}

for k, src in CHARTS.items():
    r = requests.get(f"https://www.chimet.co.uk/GetImage.ashx?src={src}", headers=H, timeout=15)
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as f:
        f.write(r.content); p = f.name
    text = subprocess.check_output(["tesseract", p, "-"]).decode()
    out[k] = [l.strip() for l in text.splitlines() if l.strip()]

json.dump(out, open("data.json", "w"), indent=2)
