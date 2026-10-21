# Ping IndexNow (Bing, Yandex, Seznam, Naver — Bing's index also feeds ChatGPT/Copilot search) with changed pages.
import json, subprocess, sys, datetime as dt, urllib.request
SITE = "https://omkiranbhakti.com/"
KEY = "5e7698afbb45a82de929a42aaf0783fe"
event = sys.argv[1] if len(sys.argv) > 1 else "push"
if event == "workflow_dispatch":
    # manual run = re-announce every URL in the sitemap (used after the domain move)
    import re
    files = None
    urls_all = re.findall(r"<loc>([^<]+)</loc>", open("sitemap.xml", encoding="utf-8").read())
elif event == "schedule":
    today = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=5, minutes=30)).date()
    files = ["index.html", "aaj-ka-panchang.html", f"panchang-{today:%Y-%m}.html", "aaj-ka-choghadiya.html", "bhadra-kaal.html", "panchak-kab-hai.html", "tyohar-kab-hai.html"]
else:
    try:
        out = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], capture_output=True, text=True).stdout.split()
    except Exception:
        out = []
    files = [f for f in out if f.endswith(".html") and "/" not in f and f != "404.html"]
    if "sitemap.xml" in out or not files: files = files or ["index.html"]
urls = urls_all[:10000] if files is None else [SITE + ("" if f == "index.html" else f) for f in dict.fromkeys(files)][:10000]
body = json.dumps({"host": "omkiranbhakti.com", "key": KEY, "keyLocation": SITE + KEY + ".txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r: print("IndexNow", r.status, len(urls), "urls")
except Exception as e:
    print("IndexNow failed:", e); sys.exit(1)
