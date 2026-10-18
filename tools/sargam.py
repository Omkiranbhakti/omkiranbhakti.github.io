"""Auto-transcribe the vocal melody of a recording into sargam (relative to the detected Sa).
usage: python3 sargam.py in.mp3 out.json [start_sec] [dur_sec]"""
import sys, json, subprocess, os, numpy as np, librosa

src, out = sys.argv[1], sys.argv[2]
start = float(sys.argv[3]) if len(sys.argv) > 3 else 0
dur = float(sys.argv[4]) if len(sys.argv) > 4 else 150
work = out + ".work"; os.makedirs(work, exist_ok=True)
clip = os.path.join(work, "clip.wav")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start), "-t", str(dur), "-i", src, "-ac", "2", "-ar", "44100", clip], check=True)
voc = os.path.join(work, "htdemucs", "clip", "vocals.wav")
if not os.path.exists(voc):
    subprocess.run([sys.executable, "-m", "demucs", "--two-stems", "vocals", "-n", "htdemucs", "-o", work, clip], check=True)

y, sr = librosa.load(voc, sr=22050, mono=True)
hop = 256
f0, vflag, vprob = librosa.pyin(y, fmin=70, fmax=900, sr=sr, hop_length=hop, frame_length=2048)
t = librosa.times_like(f0, sr=sr, hop_length=hop)
rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=hop)[0]
ok = vflag & (vprob > 0.5) & (rms[: len(f0)] > np.percentile(rms, 30))
midi = np.where(ok, librosa.hz_to_midi(np.nan_to_num(f0, nan=1.0)), np.nan)

# smooth: median over 5 frames
from scipy.ndimage import median_filter
m2 = midi.copy(); good = ~np.isnan(m2)
m2[good] = median_filter(m2[good], size=5)

# --- tonic: fit pitch-class histogram to Bilawal (major) + Sa/Pa weight; phrase-end bonus
pc = np.mod(m2[good], 12)
hist = np.zeros(1200)
for c in (pc * 100).astype(int): hist[c % 1200] += 1
hist12 = np.array([hist[(i * 100 - 40) % 1200:(i * 100 - 40) % 1200 + 80].sum() if (i * 100 - 40) % 1200 + 80 <= 1200 else hist[(i*100-40)%1200:].sum() + hist[:((i*100+40)%1200)].sum() for i in range(12)])
major = [0, 2, 4, 5, 7, 9, 11]
def score(tn):
    s = sum(hist12[(tn + d) % 12] for d in major) - 1.5 * sum(hist12[(tn + d) % 12] for d in (1, 3, 6, 8, 10))
    return s + 0.6 * hist12[tn % 12] + 0.3 * hist12[(tn + 7) % 12]

# segment notes
notes = []  # (start, end, semitone_abs)
cur = None
for i in range(len(m2)):
    v = m2[i]
    if np.isnan(v):
        if cur: notes.append(cur); cur = None
        continue
    r = int(round(v))
    if cur and r == cur[2]:
        cur[1] = t[i]
    else:
        if cur: notes.append(cur)
        cur = [t[i], t[i], r]
if cur: notes.append(cur)
notes = [n for n in notes if n[1] - n[0] >= 0.09]
# merge same consecutive notes with tiny gaps
merged = []
for n in notes:
    if merged and merged[-1][2] == n[2] and n[0] - merged[-1][1] < 0.12: merged[-1][1] = n[1]
    else: merged.append(list(n))
notes = merged
# phrases: gap > 0.35 s
phrases, ph = [], []
for n in notes:
    if ph and n[0] - ph[-1][1] > 0.35: phrases.append(ph); ph = []
    ph.append(n)
if ph: phrases.append(ph)
ends = np.zeros(12)
for p in phrases:
    if p: ends[p[-1][2] % 12] += 1
best = max(range(12), key=lambda tn: score(tn) + 0.15 * hist12.sum() / 12 * ends[tn] / max(1, ends.sum()) * 12)
# Sa absolute: choose octave so that the median melody sits in madhya saptak
med = np.nanmedian(m2)
sa = best + 12 * round((med - 4 - best) / 12)
NAMES = {0:"सा",1:"रे॒",2:"रे",3:"ग॒",4:"ग",5:"म",6:"म॑",7:"प",8:"ध॒",9:"ध",10:"नि॒",11:"नि"}
WEST = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
res = []
for p in phrases:
    row = []
    for s, e, m in p:
        rel = m - sa; oc = rel // 12; deg = rel % 12
        row.append({"n": NAMES[deg], "o": int(oc), "d": round(e - s, 2), "w": WEST[deg] + str(4 + oc), "t": round(s + start, 2)})
    res.append(row)
json.dump({"src": src, "start": start, "sa_midi": int(sa), "sa_name": librosa.midi_to_note(int(sa)), "phrases": res}, open(out, "w"), ensure_ascii=False)
print("Sa =", librosa.midi_to_note(int(sa)), "| phrases", len(res), "| notes", sum(len(r) for r in res))
for r in res[:12]:
    print(" ".join(("." if x["o"] < 0 else "") + x["n"] + ("'" if x["o"] > 0 else "") for x in r))
