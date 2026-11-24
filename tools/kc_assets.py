#!/usr/bin/env python3
"""Kaal-Chakra assets. modes: cand (image candidates + contact sheets), sound (Freesound CC0 candidates), build (picked images -> webp + credits)."""
import json,re,sys,os,time,html,urllib.parse,urllib.request,subprocess
UA={'User-Agent':'OmKiranBhakti-KaalChakra/1.0 (https://omkiranbhakti.com; bot)'}
def get(u,raw=False,tries=4,to=60):
    for t in range(tries):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=to).read()
            return r if raw else r.decode('utf8','replace')
        except Exception as e:
            time.sleep(2+3*t); err=e
    print('FAIL',u,err); return None
def api(base,**p):
    p.update(format='json',formatversion=2); s=get(base+'?'+urllib.parse.urlencode(p)); return json.loads(s) if s else {}
CA='https://commons.wikimedia.org/w/api.php'; WA='https://en.wikipedia.org/w/api.php'
def events():
    h=open('kaal-chakra/index.html',encoding='utf8').read()
    out=[]
    for m in re.finditer(r"^\[([^,]+),'(\w+)','([^']+)',.*,'([^']*)',\"([^\"]*)\"\],?$",h,re.M):
        out.append(dict(c=m[2],t=m[3],r=m[4],w=m[5],slug=re.sub(r'[^a-z0-9]+','-',m[4].lower()).strip('-')))
    return out
def info(files,w=330):
    res={}
    for i in range(0,len(files),40):
        d=api(CA,action='query',titles='|'.join(files[i:i+40]),prop='imageinfo',iiprop='url|extmetadata|size|mime',iiurlwidth=w)
        for p in d.get('query',{}).get('pages',[]):
            ii=(p.get('imageinfo') or [None])[0]
            if not ii: continue
            em=ii.get('extmetadata',{}); g=lambda k:re.sub('<[^>]+>','',html.unescape(em.get(k,{}).get('value',''))).strip()
            res[p['title']]=dict(thumb=ii.get('thumburl'),url=ii.get('url'),desc=ii.get('descriptionurl'),mime=ii.get('mime'),
              lic=g('LicenseShortName'),licurl=em.get('LicenseUrl',{}).get('value',''),artist=g('Artist')[:120],credit=g('Credit')[:120],date=g('DateTimeOriginal')[:40])
    return res
def cand():
    os.makedirs('out/th',exist_ok=True); allc={}
    done=set(json.load(open('kaal-chakra/img/pick.json'))) if os.path.exists('kaal-chakra/img/pick.json') else set()
    Q=json.load(open('tools/kc_query.json',encoding='utf8')) if os.path.exists('tools/kc_query.json') else {}
    for k,e in enumerate(events()):
        if Q:
            if e['slug'] not in Q: continue
            fs=[]
            for q in Q[e['slug']]:
                d=api(CA,action='query',list='search',srsearch=q+' filetype:bitmap',srnamespace=6,srlimit=8)
                fs+=[s['title'] for s in d.get('query',{}).get('search',[])]
            seen=[];[seen.append(f) for f in fs if f not in seen]; seen=seen[:16]
            inf=info(seen); lst=[]
            for n,f in enumerate([f for f in seen if f in inf and inf[f]['thumb']]):
                j=inf[f]; fn=f'out/th/{k:02d}_{n:02d}.jpg'; b=get(j['thumb'],raw=True)
                if not b: continue
                open(fn,'wb').write(b); j['file']=f; j['n']=n; lst.append(j)
            allc[e['slug']]=dict(k=k,t=e['t'],w=e['w'],c=lst); print(k,e['slug'],len(lst),flush=True); continue
        if e['slug'] in done or e['c']=='n': continue
        fs=[]
        if e['w']:
            d=api(WA,action='query',titles=e['w'],prop='pageimages|images',piprop='name',imlimit=40,redirects=1)
            for p in d.get('query',{}).get('pages',[]):
                if p.get('pageimage'): fs.append('File:'+p['pageimage'])
                for im in p.get('images',[]):
                    if re.search(r'\.(jpe?g|png|webp|tiff?)$',im['title'],re.I) and not re.search(r'(icon|logo|flag|map|commons-|symbol|edit|wiki|question|disamb|portal|ambox|om\.svg)',im['title'],re.I): fs.append(im['title'])
        for q in [e['w']+' painting', e['w']+' Hindu', e['r']]:
            if not e['w'] and q!=e['r']: continue
            d=api(CA,action='query',list='search',srsearch=q+' filetype:bitmap',srnamespace=6,srlimit=6)
            fs+= [s['title'] for s in d.get('query',{}).get('search',[])]
        seen=[];[seen.append(f) for f in fs if f not in seen]; seen=seen[:12]
        inf=info(seen); lst=[]
        for n,f in enumerate([f for f in seen if f in inf and inf[f]['thumb']]):
            j=inf[f]; fn=f'out/th/{k:02d}_{n:02d}.jpg'; b=get(j['thumb'],raw=True)
            if not b: continue
            open(fn,'wb').write(b); j['file']=f; j['n']=n; lst.append(j)
        allc[e['slug']]=dict(k=k,t=e['t'],w=e['w'],c=lst); print(k,e['slug'],len(lst),flush=True)
    json.dump(allc,open('out/cand.json','w'),ensure_ascii=False,indent=1)
    # contact sheets: one per event (labelled numbers), 4 events per page stacked
    os.makedirs('out/sheets',exist_ok=True)
    for slug,v in allc.items():
        k=v['k']; ims=sorted(x for x in os.listdir('out/th') if x.startswith(f'{k:02d}_'))
        if not ims: continue
        subprocess.run(['montage']+[f'out/th/{x}' for x in ims]+['-tile','6x','-geometry','220x220+4+4','-background','#222','-fill','white','-pointsize','16','-title',f'{k:02d} {slug} ({v["w"]})',f'out/sheets/{k:02d}.jpg'],check=False)
        subprocess.run(['mogrify','-quality','70',f'out/sheets/{k:02d}.jpg'])
def sound():
    os.makedirs('out/snd',exist_ok=True); res={}
    Q={'tanpura':['tanpura','tambura drone'],'bell':['temple bell','ghanta','bell india temple'],'shankh':['conch shell','shankh','sankh'],'tick':['wood block','wooden click','temple block']}
    CQ={'tanpura':['tanpura','tambura'],'bell':['temple bell','hand bell ringing','ghanta'],'shankh':['conch','shankha'],'tick':['wood block','woodblock']}
    def conv(src,fn,maxd):
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',src,'-t',str(maxd),'-ac','2','-b:a','128k',fn])
        return subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',fn],capture_output=True,text=True).stdout.strip()
    fs_ok=get('https://freesound.org/search/?q=bell',tries=1,to=25) is not None; print('freesound reachable:',fs_ok,flush=True)
    for key in Q:
        lst=[]
        if fs_ok:
            ids=[]
            for q in Q[key]:
                s=get('https://freesound.org/search/?'+urllib.parse.urlencode({'q':q,'f':'license:"Creative Commons 0"','s':'Rating highest first'}),tries=1,to=25) or ''
                for u,i in re.findall(r'/people/([^/"]+)/sounds/(\d+)/',s):
                    if i not in [x[1] for x in ids]: ids.append((u,i))
            for u,i in ids[:8]:
                p=get(f'https://freesound.org/people/{u}/sounds/{i}/',tries=1,to=25) or ''
                au=re.search(r'property="og:audio" content="([^"]+)"',p); ti=re.search(r'<title>(.*?)</title>',p,re.S)
                if not au or 'publicdomain/zero' not in p: continue
                b=get(au.group(1).replace('-lq.mp3','-hq.mp3'),raw=True,tries=1,to=40)
                if not b: continue
                open('/tmp/a','wb').write(b); fn=f'out/snd/{key}_fs{i}.mp3'; dur=conv('/tmp/a',fn,60)
                lst.append(dict(src='Freesound',id=i,user=u,title=html.unescape(ti.group(1).strip()) if ti else '',lic='CC0',dur=dur,file=os.path.basename(fn),page=f'https://freesound.org/people/{u}/sounds/{i}/'))
                if len(lst)>=4: break
        seen=set()
        for q in CQ[key]:
            d=api(CA,action='query',list='search',srsearch=q+' filetype:audio',srnamespace=6,srlimit=8)
            fl=[x['title'] for x in d.get('query',{}).get('search',[]) if x['title'] not in seen]
            if not fl: continue
            seen.update(fl); inf=info(fl)
            for f in fl:
                j=inf.get(f)
                if not j or not re.search(r'(CC0|Public domain|CC BY)',j['lic'] or '',re.I): continue
                b=get(j['url'],raw=True,tries=2,to=60)
                if not b: continue
                ext=f.rsplit('.',1)[-1]; open('/tmp/a.'+ext,'wb').write(b); fn=f'out/snd/{key}_c{len(lst)}.mp3'; dur=conv('/tmp/a.'+ext,fn,60)
                if not dur: continue
                lst.append(dict(src='Wikimedia Commons',file_c=f,title=f[5:],lic=j['lic'],licurl=j['licurl'],artist=j['artist'],dur=dur,file=os.path.basename(fn),page=j['desc']))
                if len(lst)>=7: break
            if len(lst)>=7: break
        res[key]=lst; print(key,len(lst),flush=True)
    json.dump(res,open('out/snd/sound.json','w'),ensure_ascii=False,indent=1)
def fsids():
    os.makedirs('out/snd',exist_ok=True); res={}
    for tok in os.environ.get('IDS','').split():
        key,i=tok.split(':'); p=get(f'https://freesound.org/s/{i}/',tries=2,to=30) or ''
        au=re.search(r'property="og:audio" content="([^"]+)"',p); ti=re.search(r'property="og:title" content="([^"]+)"',p) or re.search(r'<title>(.*?)</title>',p,re.S)
        us=re.search(r'freesound\.org/people/([^/"]+)/sounds/'+i,p) or re.search(r'/people/([^/"]+)/sounds/'+i,p)
        txt=re.sub('<[^>]+>',' ',p)
        lic='CC0' if ('Creative Commons 0' in txt or 'publicdomain/zero' in p) else ('CC BY-NC' if ('NonCommercial' in txt or 'by-nc' in p) else ('CC BY 4.0' if 'Attribution 4.0' in txt else ('CC BY 3.0' if ('Attribution 3.0' in txt or 'licenses/by/3.0' in p) else ('CC BY' if 'Attribution' in txt else '?'))))
        print(key,i,bool(au),lic,flush=True)
        if not au or lic in ('CC BY-NC','?'): continue
        b=get(au.group(1).replace('-lq.mp3','-hq.mp3'),raw=True,tries=2,to=60)
        if not b: continue
        fn=f'out/snd/{key}_{i}.mp3'; open(fn,'wb').write(b)
        dur=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',fn],capture_output=True,text=True).stdout.strip()
        res.setdefault(key,[]).append(dict(src='Freesound',id=i,user=us.group(1) if us else '',title=html.unescape(ti.group(1).strip()) if ti else '',lic=lic,dur=dur,file=os.path.basename(fn),page=f'https://freesound.org/s/{i}/'))
    json.dump(res,open('out/snd/sound.json','w'),ensure_ascii=False,indent=1)
def fsapi():
    os.makedirs('out/snd',exist_ok=True); res={}; key=os.environ.get('FSKEY','').strip()
    if not key: sys.exit('FREESOUND_KEY secret missing')
    for tok in os.environ.get('IDS','').split():
        cat,i=tok.split(':')
        try:
            d=json.loads(urllib.request.urlopen(urllib.request.Request(f'https://freesound.org/apiv2/sounds/{i}/?'+urllib.parse.urlencode({'token':key,'fields':'id,name,username,license,previews,duration'}),headers=UA),timeout=40).read())
        except Exception as e:
            print(cat,i,'API ERR',e,flush=True); continue
        lic=d.get('license',''); print(cat,i,d.get('name'),lic,flush=True)
        if 'nc' in lic.lower().replace('/licenses/',''): print('  skip NC'); continue
        u=d['previews']['preview-hq-mp3']
        try: b=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read()
        except Exception as e: print('  DL ERR',e,flush=True); continue
        fn=f'out/snd/{cat}_{i}.mp3'; open(fn,'wb').write(b)
        res.setdefault(cat,[]).append(dict(src='Freesound',id=i,user=d.get('username'),title=d.get('name'),lic=lic,dur=d.get('duration'),file=os.path.basename(fn),page=f'https://freesound.org/s/{i}/'))
    json.dump(res,open('out/snd/sound.json','w'),ensure_ascii=False,indent=1)
    if not res: sys.exit('no sounds fetched')
def build():
    pick=json.load(open('kaal-chakra/img/pick.json',encoding='utf8')); inf=info(list(set(pick.values())),w=640); cr={}
    for slug,f in pick.items():
        j=inf.get(f)
        if not j: print('MISSING',slug,f); continue
        b=get(j['thumb'],raw=True)
        if not b: continue
        open('/tmp/x','wb').write(b); out=f'kaal-chakra/img/{slug}.webp'
        r=subprocess.run(['convert','/tmp/x[0]','-resize','480x480>','-strip','-quality','70',out])
        if r.returncode or not os.path.exists(out): print('CONVERT FAIL',slug,f); continue
        cr[slug]=dict(file=f,desc=j['desc'],lic=j['lic'],licurl=j['licurl'],artist=j['artist'] or j['credit'] or 'Unknown',kb=os.path.getsize(out)//1024)
        print(slug,cr[slug]['kb'],'KB',flush=True)
    json.dump(cr,open('kaal-chakra/img/credits.json','w'),ensure_ascii=False,indent=1)
{'cand':cand,'sound':sound,'build':build,'fsids':fsids,'fsapi':fsapi}[sys.argv[1]]()
