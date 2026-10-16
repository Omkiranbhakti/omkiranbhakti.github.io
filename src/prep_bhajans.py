# Turn downloaded audio into web MP3s with ASCII names in audio/; audio/list.json keeps the original titles.
import sys, os, json, subprocess, hashlib
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
EXT = (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".opus", ".aif", ".aiff")
lp = os.path.join(out, "list.json"); items = json.load(open(lp)) if os.path.exists(lp) else []
have = {i["asset"] for i in items}
for root, _, files in os.walk(src):
    for f in sorted(files):
        if not f.lower().endswith(EXT): continue
        p = os.path.join(root, f); title = os.path.splitext(f)[0].strip()
        name = "b" + hashlib.md5(title.encode()).hexdigest()[:10] + ".mp3"; dst = os.path.join(out, name)
        if name in have: continue
        if f.lower().endswith(".mp3") and os.path.getsize(p) < 9 * 1048576: subprocess.run(["cp", p, dst], check=True)
        else: subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", p, "-vn", "-ac", "2", "-b:a", "128k", dst], check=True)
        dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst], capture_output=True, text=True).stdout.strip()
        items.append({"title": title, "folder": os.path.relpath(root, src), "asset": name, "mb": round(os.path.getsize(dst) / 1048576, 1), "sec": round(float(dur or 0))})
json.dump(items, open(lp, "w"), ensure_ascii=False, indent=1)
print(len(items), "files"); [print(i) for i in items]
