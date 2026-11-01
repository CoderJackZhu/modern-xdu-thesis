#!/usr/bin/env python3
"""逐输入编译并执行现有验收尺和已负向验证的 PDF 检查，保留证据。"""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import checks

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'out'

def command(args,env,timeout=120):
    try:
        p=subprocess.run(args,cwd=ROOT,env=env,capture_output=True,text=True,timeout=timeout)
        return p.returncode,p.stdout+p.stderr
    except subprocess.TimeoutExpired as e:
        return 124,'超时：'+str(args)+'\n'+str(e.stdout or '')+str(e.stderr or '')

def old_checks(c,pdf):
    k=c['kind'];d=c['degree'];out=[]
    if k=='thesis':
        if c['graduate']=='master':
            out += [('verify-front.py',['--degree',d]),('verify-front-x.py',[d])]
        else:
            opts=['--degree',d]
            if c['blind']:opts+=['--blind']
            opts+=['--no-enterprise']
            out += [('verify-doctor.py',opts)]
        out += [('verify-index.py',[]),('verify-body.py',[])]
    elif k=='bachelor':out=[('verify-undergrad.py',[])]
    else:
        out=[('verify-supporting.py',['--kind',k,'--graduate','doctor' if c['graduate']=='doctor' else 'master','--degree',d])]
    return out

def run_case(c,env):
    start=time.monotonic();pdf=OUT/(c['name']+'.pdf');log=OUT/(c['name']+'.compile.log')
    rc,msg=command(['typst','compile','--root',str(ROOT),c['source'],str(pdf)],env)
    log.write_text(msg)
    r=dict(c,compile_rc=rc,compile_errors=[x for x in msg.splitlines() if x.startswith('error:')],warnings=[x for x in msg.splitlines() if x.startswith('warning:')],legacy=[],general=None)
    if rc==0:
        for script,opts in old_checks(c,pdf):
            code,text=command(['python3',str(ROOT/'dev'/script),str(pdf)]+opts,env,60)
            (OUT/(c['name']+'.'+script+'.log')).write_text(text)
            r['legacy'].append(dict(script=script,rc=code))
        try:r['general']=checks.inspect(pdf,c)
        except Exception as e:r['general']=dict(error=repr(e))
        (OUT/(c['name']+'.checks.json')).write_text(json.dumps(r['general'],ensure_ascii=False,indent=2)+'\n')
    r['elapsed']=round(time.monotonic()-start,2)
    r['source_sha256']=hashlib.sha256((ROOT/c['source']).read_bytes()).hexdigest()
    return r

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--round',type=int,default=1);ap.add_argument('--workers',type=int,default=5);ap.add_argument('--only');ap.add_argument('--recheck',action='store_true');a=ap.parse_args()
    OUT.mkdir(exist_ok=True)
    package=OUT/'packages/preview/modern-xdu-thesis/0.3.1';package.parent.mkdir(parents=True,exist_ok=True)
    if not package.exists():package.symlink_to(ROOT)
    assert package.resolve()==ROOT
    env=dict(os.environ,TYPST_PACKAGE_PATH=str(OUT/'packages'),PYTHONDONTWRITEBYTECODE='1')
    cases=json.loads((HERE/f'manifest-r{a.round:02}.json').read_text())
    if a.only:cases=[c for c in cases if a.only in c['name']]
    start=time.monotonic();results=[]
    if a.recheck:
        for c in cases:
            pdf=OUT/(c['name']+'.pdf')
            if pdf.exists():
                result=checks.inspect(pdf,c);(OUT/(c['name']+'.checks.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        return
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
        futures=[pool.submit(run_case,c,env) for c in cases]
        for f in concurrent.futures.as_completed(futures):
            results.append(f.result())
            if len(results)%20==0:print(f'第{a.round}轮 {len(results)}/{len(cases)}，编译失败{sum(x["compile_rc"]!=0 for x in results)}，耗时{time.monotonic()-start:.0f}s',flush=True)
    result=dict(round=a.round,base=command(['git','rev-parse','origin/main'],env)[1].strip(),elapsed=round(time.monotonic()-start,2),cases=sorted(results,key=lambda x:x['name']))
    (HERE/f'results-r{a.round:02}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f'完成第{a.round}轮：{len(results)}份，{result["elapsed"]}秒',flush=True)

if __name__=='__main__':main()
